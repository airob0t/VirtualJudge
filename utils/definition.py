class JudgeRequest:
    status = {
        "PENDING": 0,
        "JUDGING": 1,
        "SUCCESS": 2,
        "SEND_FOR_JUDGE_ERROR": 3,
        "RETRY": 4,
    }


class ProblemRequest:
    status = {
        "PENDING": 0,
        "CRAWLING": 1,
        "SUCCESS": 2,
        "ERROR": 3,
        "RETRY": 4
    }


class Message(object):
    DEFAULT = 0
    SUCCESS = 1
    WARNING = 2
    ERROR = 3
    INFO = 4


def success(information):
    return {
        'status': Message.SUCCESS,
        'message': information
    }


def warning(information):
    return {
        'status': Message.WARNING,
        'message': information
    }


def error(information):
    return {
        'status': Message.ERROR,
        'message': information
    }


def info(information):
    return {
        'status': Message.INFO,
        'message': information
    }


def default(information):
    return {
        'status': Message.DEFAULT,
        'message': information
    }