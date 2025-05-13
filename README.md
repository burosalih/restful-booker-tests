
# 🧪 RESTful Booker API Tests

**Base URL:** `https://restful-booker.herokuapp.com`  
**Date:** May 13, 2025  
**Tested By:** Salih Buro
**Tools Used:** `pytest`, `requests`  

---

## ✅ Test Summary

| Test Case ID     | Test Description                                | Status  |
|------------------|--------------------------------------------------|---------|
| TC-SM-01         | Health check and auth                            | ✅ Pass |
| TC-SM-02         | Create → Get → Delete booking                    | ✅ Pass (with bugs noted) |
| TC-SM-03         | Get all bookings                                 | ✅ Pass |
| TC-CR-01         | Create booking with valid data                   | ✅ Pass (with bugs noted) |
| TC-CR-02         | Create booking with missing required fields      | ✅ Pass |
| TC-DL-01         | Delete existing booking                          | ✅ Pass (with bugs noted) |
| TC-DL-02         | Delete booking with invalid ID                   | ✅ Pass (with bugs noted) |

---

## 🐞 Known Bugs & Issues

| Bug ID | Endpoint                              | Description                                                                                                                                      | Severity | Expected Behavior                |
|--------|----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|----------|----------------------------------|
| BUG-001 | `POST /booking`                       | `totalprice` does **not support float** accurately – values like `99.99` get truncated or rounded unexpectedly                                 | Medium   | Float values should persist     |
| BUG-002 | `POST /booking`                       | Invalid `checkin`/`checkout` dates are rejected but return **200 OK** instead of **400 Bad Request**                                           | Medium   | Return `400` for validation fail|
| BUG-003 | `DELETE /booking/{id}`                | **Authorization via `Authorization: Bearer <token>` header fails** – only `Cookie` is accepted                                                  | Medium   | Both Cookie & Bearer accepted  |
| BUG-004 | `DELETE /booking/{id}`                | Returns **201 Created** on success — not appropriate for DELETE                                                                                 | High     | Should return `204 No Content` |
| BUG-005 | `DELETE /booking/{invalid_id}`        | Returns **405 Method Not Allowed** for invalid ID — should return **404 Not Found**                                                             | Medium   | Return `404` if not exists     |
| BUG-006 | `GET /ping`                           | Returns **201 Created** — misleading for a health check                                                                                         | Low      | Should return `200 OK`         |

---

## 🔎 Observations

- All CRUD operations functionally **work**, but **status codes and header handling** are inconsistent with RESTful best practices.
- The **token-based authentication** implementation is limited and could benefit from **support for Authorization headers**.

---

## 📋 Recommendations

1. **Fix HTTP status codes** to align with REST conventions:
   - `201` → `204` for DELETE
   - `201` → `200` for `/ping`
   - `405` → `404` for missing resources

2. **Support Bearer Token authentication** via `Authorization` header.

---

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Tests

To run the test suite, navigate to the project root and run:

```bash
python -m pytest -v
```

To include extra logging or debugging:

```bash
python -m pytest -v -rA
```

---

## 🧑‍💻 Notes

This test suite is designed for educational purposes to demonstrate skills in API testing, exploratory testing, and reporting. Improvements welcome!
