import requests

def get_version():
    try:
        url = "https://api.github.com/repos/username/repo/releases/latest"  # Replace with your repo URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        latest_release = response.json()

        if 'tag_name' in latest_release:
            return latest_release['tag_name']
        else:
            return "Unknown"
    except requests.exceptions.RequestException as e:
        print(f"GitHub Error: {e}")
        return "Unknown"
