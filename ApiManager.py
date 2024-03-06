import requests

class ApiManager:
    token = 'notionToken'
    databaseID ="Notion database id"

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    @staticmethod
    def get_pages(num_pages=None):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        """
        url = f"https://api.notion.com/v1/databases/{ApiManager.databaseID}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=ApiManager.headers)

        data = response.json()

        results = data["results"]
        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            url = f"https://api.notion.com/v1/databases/{ApiManager.databaseID}/query"
            response = requests.post(url, json=payload, headers=ApiManager.headers)
            data = response.json()
            results.extend(data["results"])

        return results
