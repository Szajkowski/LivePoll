# tests/test_polls_api.py
import pytest

@pytest.fixture
def poll_payload():
    return {
        "title": "Test Poll",
        "questions": [
            {
                "text": "What is your favorite color?",
                "type": "single",
                "answers": [
                    {"text": "Red"},
                    {"text": "Blue"},
                    {"text": "Green"}
                ]
            }
        ]
    }

def test_create_poll(client, poll_payload):
    res = client.post("/polls/", json=poll_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert "poll_id" in data

def test_get_poll(client, poll_payload):
    res_create = client.post("/polls/", json=poll_payload)
    poll_id = res_create.json()["poll_id"]

    res = client.get(f"/polls/{poll_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == poll_id
    assert data["title"] == poll_payload["title"]
    assert len(data["questions"]) == 1
    assert len(data["questions"][0]["answers"]) == 3

def test_poll_results(client, poll_payload):
    res_create = client.post("/polls/", json=poll_payload)
    poll_id = res_create.json()["poll_id"]

    res = client.get(f"/polls/{poll_id}/results")
    assert res.status_code == 200
    results = res.json()
    assert len(results) == 1
    assert results[0]["text"] == poll_payload["questions"][0]["text"]
    for a in results[0]["answers"]:
        assert a["votes"] == 0

def test_update_poll(client, poll_payload):
    res_create = client.post("/polls/", json=poll_payload)
    poll_id = res_create.json()["poll_id"]

    poll_data = client.get(f"/polls/{poll_id}").json()
    question_id = poll_data["questions"][0]["id"]
    answer_id = poll_data["questions"][0]["answers"][0]["id"]

    update_payload = {
        "title": "Updated Poll Title",
        "questions": [
            {
                "id": question_id,
                "text": "Updated question?",
                "type": "single",
                "answers": [
                    {"id": answer_id, "text": "Updated answer"},
                    {"id": None, "text": "New answer"}
                ]
            }
        ]
    }

    res = client.patch(f"/polls/{poll_id}", json=update_payload)
    assert res.status_code == 200, res.json()  # pokaż dokładny błąd jeśli 422
    data = res.json()
    assert data["title"] == "Updated Poll Title"
    assert len(data["questions"][0]["answers"]) == 2


def test_delete_poll(client, poll_payload):
    res = client.post("/polls/", json=poll_payload)
    assert res.status_code == 200
    poll_id = res.json()["poll_id"]

    delete_payload = {"type": "poll", "id": poll_id}

    # trzeba jawnie podać headers={"Content-Type": "application/json"} z jakiegoś dziwnego powodu
    res2 = client.request(
        "DELETE",
        "/polls/delete",
        json=delete_payload,
        headers={"Content-Type": "application/json"}
    )

    assert res2.status_code == 200
    assert res2.json() == {"deleted": "poll"}

    res3 = client.get(f"/polls/{poll_id}")
    assert res3.status_code == 404

