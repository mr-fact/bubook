from mongoengine import get_db


def get_technical_reports(**kwargs):
    db = get_db()
    collection = db["technical_reports"]
    result = collection.find(kwargs)
    technical_reports = list(result)
    for technical_report in technical_reports:
        technical_report["_id"] = str(technical_report["_id"])
        technical_report["created_at"] = str(technical_report["created_at"])
    return technical_reports


def get_created_technical_reports(**kwargs):
    return get_technical_reports(status='created', **kwargs)
