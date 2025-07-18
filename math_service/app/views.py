# math_service/app/views.py
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.models import OperationRequest, JobStatusResponse, OperationResponse
from app.cache import OperationCache
from app.database import Database
from app.worker import JobQueue
#from flask import render_template_string


# Create a Flask Blueprint for the API
api = Blueprint('api', __name__)
cache = OperationCache()
db = Database()
job_queue = JobQueue(cache, db)

@api.route('/api/operation', methods=['POST'])
def submit_operation():
    try:
        data = request.get_json()
        op_req = OperationRequest(**data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 422

    # Validate operands length
    if op_req.op_type == "pow" and len(op_req.operands) != 2:
        return jsonify({'error': 'pow needs 2 operands'}), 400
    if op_req.op_type in ("fibonacci", "factorial") and len(op_req.operands) != 1:
        return jsonify({'error': f'{op_req.op_type} needs 1 operand'}), 400

    job_id = job_queue.submit(op_req.op_type, op_req.operands)
    return jsonify({"job_id": job_id, "status": "PENDING"}), 202

@api.route('/api/operation/<job_id>', methods=['GET'])
def get_status(job_id):
    job = job_queue.get_status(job_id)
    resp = JobStatusResponse(
        job_id=job_id,
        status=job.get("status", "NOT_FOUND"),
        result=job.get("result"),
        error=job.get("error")
    )
    return jsonify(resp.dict()), 200 if job["status"] != "NOT_FOUND" else 404

@api.route('/api/history', methods=['GET'])
def get_history():
    reqs = db.fetch_all_requests()
    history = [
        OperationResponse(
            result=row[2],
            op_type=row[0],
            operands=eval(row[1]),
            timestamp=row[3]
        ).dict()
        for row in reqs
    ]
    return jsonify(history), 200

@api.route('/health', methods=['GET'])
def health():
    return "OK", 200
