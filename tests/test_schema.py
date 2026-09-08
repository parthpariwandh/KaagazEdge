from app.schema_validate import available_schemas, validate_record


def test_schemas_present():
    names = available_schemas()
    for required in ("invoice", "marksheet", "clinic_report", "job_card"):
        assert required in names


def test_invoice_valid():
    record = {
        "document_type": "gst_invoice",
        "language": "en",
        "confidence": 0.7,
        "supplier_name": "Sample Traders Kolkata",
        "grand_total": 11800.0,
    }
    assert validate_record("invoice", record) == []


def test_invoice_rejects_bad_language():
    record = {"document_type": "gst_invoice", "language": "fr", "confidence": 0.7}
    errors = validate_record("invoice", record)
    assert errors
