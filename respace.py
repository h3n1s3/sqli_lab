from lib.core.enums import PRIORITY
__priority__ = PRIORITY.NORMAL

def tamper(payload , **kwargs):
    if payload:
        payload = payload.replace(" " , "/**/")
    return payload
