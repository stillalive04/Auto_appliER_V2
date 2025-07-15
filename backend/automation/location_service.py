from typing import List, Dict

class LocationService:
    def __init__(self):
        self.us_states = {
            "AL": {"name": "Alabama", "major_cities": ["Birmingham", "Montgomery", "Mobile", "Huntsville"]},
            "AK": {"name": "Alaska", "major_cities": ["Anchorage", "Fairbanks", "Juneau"]},
            "AZ": {"name": "Arizona", "major_cities": ["Phoenix", "Tucson", "Mesa", "Chandler", "Scottsdale"]},
            "AR": {"name": "Arkansas", "major_cities": ["Little Rock", "Fort Smith", "Fayetteville"]},
            "CA": {"name": "California", "major_cities": ["Los Angeles", "San Francisco", "San Diego", "San Jose", "Sacramento", "Oakland", "Palo Alto", "Mountain View", "Menlo Park"]},
            "CO": {"name": "Colorado", "major_cities": ["Denver", "Colorado Springs", "Aurora", "Boulder"]},
            "CT": {"name": "Connecticut", "major_cities": ["Hartford", "New Haven", "Stamford", "Bridgeport"]},
            "DE": {"name": "Delaware", "major_cities": ["Wilmington", "Dover", "Newark"]},
            "FL": {"name": "Florida", "major_cities": ["Miami", "Orlando", "Tampa", "Jacksonville", "Fort Lauderdale"]},
            "GA": {"name": "Georgia", "major_cities": ["Atlanta", "Augusta", "Columbus", "Savannah"]},
            "HI": {"name": "Hawaii", "major_cities": ["Honolulu", "Hilo", "Kailua"]},
            "ID": {"name": "Idaho", "major_cities": ["Boise", "Meridian", "Nampa"]},
            "IL": {"name": "Illinois", "major_cities": ["Chicago", "Aurora", "Peoria", "Rockford"]},
            "IN": {"name": "Indiana", "major_cities": ["Indianapolis", "Fort Wayne", "Evansville"]},
            "IA": {"name": "Iowa", "major_cities": ["Des Moines", "Cedar Rapids", "Davenport"]},
            "KS": {"name": "Kansas", "major_cities": ["Wichita", "Overland Park", "Kansas City"]},
            "KY": {"name": "Kentucky", "major_cities": ["Louisville", "Lexington", "Bowling Green"]},
            "LA": {"name": "Louisiana", "major_cities": ["New Orleans", "Baton Rouge", "Shreveport"]},
            "ME": {"name": "Maine", "major_cities": ["Portland", "Lewiston", "Bangor"]},
            "MD": {"name": "Maryland", "major_cities": ["Baltimore", "Annapolis", "Frederick"]},
            "MA": {"name": "Massachusetts", "major_cities": ["Boston", "Worcester", "Springfield", "Cambridge"]},
            "MI": {"name": "Michigan", "major_cities": ["Detroit", "Grand Rapids", "Warren", "Ann Arbor"]},
            "MN": {"name": "Minnesota", "major_cities": ["Minneapolis", "Saint Paul", "Rochester"]},
            "MS": {"name": "Mississippi", "major_cities": ["Jackson", "Gulfport", "Southaven"]},
            "MO": {"name": "Missouri", "major_cities": ["Kansas City", "Saint Louis", "Springfield"]},
            "MT": {"name": "Montana", "major_cities": ["Billings", "Missoula", "Great Falls"]},
            "NE": {"name": "Nebraska", "major_cities": ["Omaha", "Lincoln", "Bellevue"]},
            "NV": {"name": "Nevada", "major_cities": ["Las Vegas", "Henderson", "Reno"]},
            "NH": {"name": "New Hampshire", "major_cities": ["Manchester", "Nashua", "Concord"]},
            "NJ": {"name": "New Jersey", "major_cities": ["Newark", "Jersey City", "Paterson", "Princeton"]},
            "NM": {"name": "New Mexico", "major_cities": ["Albuquerque", "Las Cruces", "Rio Rancho"]},
            "NY": {"name": "New York", "major_cities": ["New York City", "Buffalo", "Rochester", "Yonkers", "Syracuse", "Albany"]},
            "NC": {"name": "North Carolina", "major_cities": ["Charlotte", "Raleigh", "Greensboro", "Durham"]},
            "ND": {"name": "North Dakota", "major_cities": ["Fargo", "Bismarck", "Grand Forks"]},
            "OH": {"name": "Ohio", "major_cities": ["Columbus", "Cleveland", "Cincinnati", "Toledo"]},
            "OK": {"name": "Oklahoma", "major_cities": ["Oklahoma City", "Tulsa", "Norman"]},
            "OR": {"name": "Oregon", "major_cities": ["Portland", "Salem", "Eugene"]},
            "PA": {"name": "Pennsylvania", "major_cities": ["Philadelphia", "Pittsburgh", "Allentown", "Erie"]},
            "RI": {"name": "Rhode Island", "major_cities": ["Providence", "Cranston", "Warwick"]},
            "SC": {"name": "South Carolina", "major_cities": ["Columbia", "Charleston", "North Charleston"]},
            "SD": {"name": "South Dakota", "major_cities": ["Sioux Falls", "Rapid City", "Aberdeen"]},
            "TN": {"name": "Tennessee", "major_cities": ["Nashville", "Memphis", "Knoxville", "Chattanooga"]},
            "TX": {"name": "Texas", "major_cities": ["Houston", "San Antonio", "Dallas", "Austin", "Fort Worth", "El Paso", "Arlington", "Plano"]},
            "UT": {"name": "Utah", "major_cities": ["Salt Lake City", "West Valley City", "Provo"]},
            "VT": {"name": "Vermont", "major_cities": ["Burlington", "Essex", "South Burlington"]},
            "VA": {"name": "Virginia", "major_cities": ["Virginia Beach", "Norfolk", "Chesapeake", "Richmond", "Alexandria"]},
            "WA": {"name": "Washington", "major_cities": ["Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue", "Redmond"]},
            "WV": {"name": "West Virginia", "major_cities": ["Charleston", "Huntington", "Parkersburg"]},
            "WI": {"name": "Wisconsin", "major_cities": ["Milwaukee", "Madison", "Green Bay"]},
            "WY": {"name": "Wyoming", "major_cities": ["Cheyenne", "Casper", "Laramie"]},
            "DC": {"name": "District of Columbia", "major_cities": ["Washington"]}
        }
        
        self.canada_provinces = {
            "AB": {"name": "Alberta", "major_cities": ["Calgary", "Edmonton", "Red Deer"]},
            "BC": {"name": "British Columbia", "major_cities": ["Vancouver", "Victoria", "Surrey", "Burnaby"]},
            "MB": {"name": "Manitoba", "major_cities": ["Winnipeg", "Brandon", "Steinbach"]},
            "NB": {"name": "New Brunswick", "major_cities": ["Saint John", "Moncton", "Fredericton"]},
            "NL": {"name": "Newfoundland and Labrador", "major_cities": ["St. John's", "Corner Brook", "Mount Pearl"]},
            "NS": {"name": "Nova Scotia", "major_cities": ["Halifax", "Sydney", "Truro"]},
            "ON": {"name": "Ontario", "major_cities": ["Toronto", "Ottawa", "Mississauga", "Brampton", "Hamilton", "London", "Markham", "Vaughan", "Kitchener", "Windsor"]},
            "PE": {"name": "Prince Edward Island", "major_cities": ["Charlottetown", "Summerside", "Stratford"]},
            "QC": {"name": "Quebec", "major_cities": ["Montreal", "Quebec City", "Laval", "Gatineau", "Longueuil"]},
            "SK": {"name": "Saskatchewan", "major_cities": ["Saskatoon", "Regina", "Prince Albert"]},
            "NT": {"name": "Northwest Territories", "major_cities": ["Yellowknife", "Hay River", "Inuvik"]},
            "NU": {"name": "Nunavut", "major_cities": ["Iqaluit", "Rankin Inlet", "Arviat"]},
            "YT": {"name": "Yukon", "major_cities": ["Whitehorse", "Dawson City", "Watson Lake"]}
        }
    
    def get_us_locations(self) -> List[Dict[str, str]]:
        """Get all US states and major cities"""
        locations = []
        
        # Add country-wide option
        locations.append({"value": "US", "label": "United States (All)", "type": "country"})
        
        # Add states with major cities
        for code, info in self.us_states.items():
            # Add state
            locations.append({
                "value": f"US-{code}",
                "label": f"{info['name']}, US",
                "type": "state"
            })
            
            # Add major cities
            for city in info['major_cities']:
                locations.append({
                    "value": f"{city}, {info['name']}, US",
                    "label": f"{city}, {info['name']}, US",
                    "type": "city"
                })
        
        return locations
    
    def get_canada_locations(self) -> List[Dict[str, str]]:
        """Get all Canadian provinces and major cities"""
        locations = []
        
        # Add country-wide option
        locations.append({"value": "CA", "label": "Canada (All)", "type": "country"})
        
        # Add provinces with major cities
        for code, info in self.canada_provinces.items():
            # Add province
            locations.append({
                "value": f"CA-{code}",
                "label": f"{info['name']}, Canada",
                "type": "province"
            })
            
            # Add major cities
            for city in info['major_cities']:
                locations.append({
                    "value": f"{city}, {info['name']}, Canada",
                    "label": f"{city}, {info['name']}, Canada",
                    "type": "city"
                })
        
        return locations
    
    def get_all_locations(self) -> List[Dict[str, str]]:
        """Get all locations (US and Canada)"""
        locations = []
        
        # Add global option
        locations.append({"value": "ALL", "label": "United States & Canada (All)", "type": "global"})
        
        # Add US locations
        locations.extend(self.get_us_locations())
        
        # Add Canada locations
        locations.extend(self.get_canada_locations())
        
        return locations
    
    def get_major_tech_hubs(self) -> List[Dict[str, str]]:
        """Get major tech hub locations"""
        tech_hubs = [
            {"value": "San Francisco, California, US", "label": "San Francisco, CA (Silicon Valley)", "type": "tech_hub"},
            {"value": "Seattle, Washington, US", "label": "Seattle, WA", "type": "tech_hub"},
            {"value": "New York City, New York, US", "label": "New York City, NY", "type": "tech_hub"},
            {"value": "Austin, Texas, US", "label": "Austin, TX", "type": "tech_hub"},
            {"value": "Boston, Massachusetts, US", "label": "Boston, MA", "type": "tech_hub"},
            {"value": "Los Angeles, California, US", "label": "Los Angeles, CA", "type": "tech_hub"},
            {"value": "Chicago, Illinois, US", "label": "Chicago, IL", "type": "tech_hub"},
            {"value": "Denver, Colorado, US", "label": "Denver, CO", "type": "tech_hub"},
            {"value": "Atlanta, Georgia, US", "label": "Atlanta, GA", "type": "tech_hub"},
            {"value": "Toronto, Ontario, Canada", "label": "Toronto, ON", "type": "tech_hub"},
            {"value": "Vancouver, British Columbia, Canada", "label": "Vancouver, BC", "type": "tech_hub"},
            {"value": "Montreal, Quebec, Canada", "label": "Montreal, QC", "type": "tech_hub"},
        ]
        
        return tech_hubs 