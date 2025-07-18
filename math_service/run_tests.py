import requests
import time

BASE = "http://localhost:5000"

def post_operation(payload):
    r = requests.post(f"{BASE}/api/operation", json=payload)
    assert r.status_code == 202
    job_id = r.json()["job_id"]
    print(f"[POST] Sent: {payload} -> job_id: {job_id}")
    return job_id

def wait_for_result(job_id):
    url = f"{BASE}/api/operation/{job_id}"
    for i in range(10):
        r = requests.get(url)
        data = r.json()
        if data.get("status") in ("DONE", "OK"):
            print(f"[GET ] Result for job_id {job_id}: {data['result']}")
            return data["result"]
        print(f"[GET ] job_id {job_id} not ready yet ({data['status']}), waiting...")
        time.sleep(0.5)
    print(f"[GET ] job_id {job_id} did not finish in time!")
    return None

def test_factorial_5():
    job_id = post_operation({"op_type": "factorial", "operands": [5]})
    res = wait_for_result(job_id)
    assert res == 120

def test_pow_2_10():
    job_id = post_operation({"op_type": "pow", "operands": [2, 10]})
    res = wait_for_result(job_id)
    assert res == 1024

def test_fibonacci_8():
    job_id = post_operation({"op_type": "fibonacci", "operands": [8]})
    res = wait_for_result(job_id)
    assert res == 21

def test_error_invalid_op():
    r = requests.post(f"{BASE}/api/operation", json={"op_type": "sqrt", "operands": [4]})
    print(f"[POST] Invalid op response status: {r.status_code}, body: {r.text}")
    assert r.status_code == 400
    print("[POST] Invalid operation caught OK.")


def test_history():
    r = requests.get(f"{BASE}/api/history")
    assert r.status_code == 200
    history = r.json()
    print(f"[HIST] Found {len(history)} history entries.")

if __name__ == "__main__":
    print("=== Math Microservice Simple Tests ===")
    test_factorial_5()
    test_pow_2_10()
    test_fibonacci_8()
    test_error_invalid_op()
    test_history()
    print("=== DONE ===")
