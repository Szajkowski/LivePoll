# tests/test_votes_api.py
import pytest

def test_vote_once(client):
    payload = {
        "title": "Poll for Voting",
        "questions": [
            {
                "text": "Favorite color?",
                "type": "single",
                "answers": [{"text": "Red"}, {"text": "Blue"}]
            }
        ]
    }
    res = client.post("/polls/", json=payload)
    poll_id = res.json()["poll_id"]

    # --- pobierz pytanie i odpowiedź z bazy ---
    poll_data = client.get(f"/polls/{poll_id}").json()
    question_id = poll_data["questions"][0]["id"]
    answer_id = poll_data["questions"][0]["answers"][0]["id"]

    # --- zagłosuj ---
    vote_payload = {
        "votes": [
            {
                "poll_id": poll_id,
                "question_id": question_id,
                "answer_id": answer_id,
                "session_id": "sess_1"
            }
        ]
    }
    vote_res = client.post("/votes/", json=vote_payload)
    assert vote_res.status_code == 200
    data = vote_res.json()
    assert data["status"] == "ok"

def test_vote_twice_ignored(client):
    payload = {
        "title": "Poll for Double Voting",
        "questions": [
            {
                "text": "Favorite food?",
                "type": "single",
                "answers": [{"text": "Pizza"}, {"text": "Sushi"}]
            }
        ]
    }
    res = client.post("/polls/", json=payload)
    poll_id = res.json()["poll_id"]

    poll_data = client.get(f"/polls/{poll_id}").json()
    question_id = poll_data["questions"][0]["id"]
    answer_id = poll_data["questions"][0]["answers"][0]["id"]

    vote_payload = {
        "votes": [
            {
                "poll_id": poll_id,
                "question_id": question_id,
                "answer_id": answer_id,
                "session_id": "sess_2"
            }
        ]
    }

    # --- pierwszy głos ---
    vote_res1 = client.post("/votes/", json=vote_payload)
    assert vote_res1.json()["status"] == "ok"

    # --- drugi głos (ten sam session_id) ---
    vote_res2 = client.post("/votes/", json=vote_payload)
    assert vote_res2.json()["status"] == "ignored"
    assert vote_res2.json()["reason"] == "already_voted"
