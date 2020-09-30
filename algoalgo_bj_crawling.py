import requests
from bs4 import BeautifulSoup


def getBJSolved(username):
    url = f"https://www.acmicpc.net/user/{username}"

    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    # class panel-title : 맞은 문제
    # class problem_number

    all_clear = []
    match_problem = soup.find(class_="panel-body")
    problems = match_problem.find_all("span", class_ = "problem_number")

    for p in problems:
        p = p.find("a")
        all_clear.append(p.get_text())

    all_clear_str = ""
    for ac in all_clear:
        all_clear_str += ac
        all_clear_str += ";"

    return all_clear_str