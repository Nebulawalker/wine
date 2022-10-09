import datetime


COMPANY_FOUNDATION_YEAR = 1920


def get_company_age() -> str:
    current_year = datetime.datetime.now().year
    delta = current_year - COMPANY_FOUNDATION_YEAR

    if delta % 100 >= 11 and delta % 100 <= 14:
        ending = "лет"
    elif delta % 10 == 1:
        ending = "год"
    elif delta % 10 in (2, 3, 4):
        ending = "года"
    else:
        ending = "лет"
    company_age = f"{delta} {ending}"

    return company_age
