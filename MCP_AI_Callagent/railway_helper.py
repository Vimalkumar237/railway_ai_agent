"""
Helper module to interface with Indian Railway MCP tools
"""

def search_trains(from_station, to_station, date):
    """
    Search for trains between two stations
    """
    try:
        # This would normally call the MCP function
        # For now, we'll use a direct API call to the Indian Railway service
        import requests
        
        # Use the Indian Railway API directly
        url = "https://railway-mcp.amithv.xyz/mcp/search"
        payload = {
            "from_station": from_station.upper(),
            "to_station": to_station.upper(),
            "date": date
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        return {"error": str(e)}

def get_train_live_status(train_no, date):
    """
    Get live status of a train
    """
    try:
        import requests
        
        url = "https://railway-mcp.amithv.xyz/mcp/live-status"
        payload = {
            "train_no": train_no,
            "date": date
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        return {"error": str(e)}

def get_station_code(station_name):
    """
    Get station code from station name
    """
    try:
        import requests
        
        url = "https://railway-mcp.amithv.xyz/mcp/station-code"
        payload = {
            "station_name": station_name
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        return {"error": str(e)}

