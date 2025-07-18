import requests
import time

BASE_URL = "http://localhost:5000"

def test_healthcheck():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    assert r.text == "OK"

def post_job(payload):
    r = requests.post(f"{BASE_URL}/api/operation", json=payload)
    assert r.status_code == 202
    return r.json()["job_id"]

def get_job_result(job_id):
    for _ in range(10):  # Așteaptă până la 5 secunde
        r = requests.get(f"{BASE_URL}/api/operation/{job_id}")
        if r.status_code == 200 and r.json()["status"] == "DONE":
            return r.json()["result"]
        time.sleep(0.5)
    raise Exception("Job not completed in time!")

def test_factorial_5():
    job_id = post_job({"op_type": "factorial", "operands": [5]})
    assert get_job_result(job_id) == 120

def test_pow_2_10():
    job_id = post_job({"op_type": "pow", "operands": [2, 10]})
    assert get_job_result(job_id) == 1024

def test_fibonacci_12():
    job_id = post_job({"op_type": "fibonacci", "operands": [12]})
    assert get_job_result(job_id) == 144

def test_error_wrong_operands():
    r = requests.post(f"{BASE_URL}/api/operation", json={"op_type": "pow", "operands": [2]})
    assert r.status_code == 400

def test_error_invalid_op():
    r = requests.post(f"{BASE_URL}/api/operation", json={"op_type": "square_root", "operands": [4]})
    assert r.status_code == 400

def test_history():
    r = requests.get(f"{BASE_URL}/api/history")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) > 0  # Asigură-te că există cel puțin o intrare în istoric