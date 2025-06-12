from faker import Faker
from typing import List, Dict, Any, Optional
from datetime import datetime
from functools import lru_cache
import uuid
import csv
import json
import xml.etree.ElementTree as ET
from io import StringIO
from config import get_settings
from schemas import ExportFormat

settings = get_settings()

class UserGenerator:
    """Enhanced user data generation service."""
    
    def __init__(self, locale: str = settings.DEFAULT_LOCALE):
        self.fake = Faker(locale)
        
    @lru_cache(maxsize=100)
    def _generate_username(self, name: str) -> str:
        """Generate a username from full name."""
        return name.lower().replace(" ", "_")
    
    def _generate_social_media(self) -> Dict[str, str]:
        """Generate social media profiles."""
        return {
            "linkedin": f"https://linkedin.com/in/{self.fake.user_name()}",
            "twitter": f"https://twitter.com/{self.fake.user_name()}",
            "facebook": f"https://facebook.com/{self.fake.user_name()}"
        }
    
    def _generate_education(self) -> List[Dict[str, Any]]:
        """Generate education history."""
        universities = [
            "Stanford University",
            "MIT",
            "Harvard University",
            "Oxford University",
            "Cambridge University",
            "Yale University",
            "Princeton University"
        ]
        education = []
        for _ in range(self.fake.random_int(1, 3)):
            education.append({
                "degree": self.fake.random_element(["Bachelor's", "Master's", "PhD"]),
                "field": self.fake.random_element(["Computer Science", "Business", "Engineering", "Arts"]),
                "institution": self.fake.random_element(universities),
                "year": self.fake.random_int(2000, 2023)
            })
        return education
    
    def _generate_credit_card(self) -> Dict[str, str]:
        """Generate credit card information."""
        return {
            "number": f"****-****-****-{self.fake.credit_card_number()[-4:]}",
            "expiry": f"{self.fake.credit_card_expire()}",
            "type": self.fake.credit_card_provider()
        }

    def generate_user(self) -> Dict[str, Any]:
        """Generate a single user with enhanced data."""
        name = self.fake.name()
        company = self.fake.company()
        
        return {
            "name": name,
            "email": self.fake.email(),
            "address": self.fake.address(),
            "phone": self.fake.phone_number(),
            "job": self.fake.job(),
            "birthdate": self.fake.date_of_birth(minimum_age=18, maximum_age=90),
            "company": company,
            "username": self._generate_username(name),
            "website": self.fake.url(),
            "avatar_url": f"https://avatars.dicebear.com/api/human/{uuid.uuid4()}.svg",
            "social_media": self._generate_social_media(),
            "skills": self.fake.random_elements(
                elements=("Python", "JavaScript", "Java", "C++", "SQL", "React", "Node.js", "Docker"),
                length=self.fake.random_int(2, 6)
            ),
            "education": self._generate_education(),
            "languages": self.fake.random_elements(
                elements=("English", "Spanish", "French", "German", "Chinese", "Japanese"),
                length=self.fake.random_int(1, 3)
            ),
            "credit_card": self._generate_credit_card()
        }
    
    def generate_users(self, count: int) -> List[Dict[str, Any]]:
        """Generate multiple users."""
        if count > settings.MAX_USERS_PER_REQUEST:
            count = settings.MAX_USERS_PER_REQUEST
            
        return [self.generate_user() for _ in range(count)]
    
    def generate_users_by_country(self, country_code: str, count: int) -> List[Dict[str, Any]]:
        """Generate users for a specific country."""
        original_fake = self.fake
        self.fake = Faker(country_code)
        users = self.generate_users(count)
        self.fake = original_fake
        return users
    
    def export_users(self, users: List[Dict[str, Any]], format: ExportFormat, include_fields: Optional[List[str]] = None) -> str:
        """Export users in specified format."""
        if include_fields:
            users = [{k: v for k, v in user.items() if k in include_fields} for user in users]
            
        if format == ExportFormat.JSON:
            return json.dumps(users, indent=2, default=str)
            
        elif format == ExportFormat.CSV:
            output = StringIO()
            if not users:
                return ""
            fieldnames = users[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                writer.writerow({k: str(v) for k, v in user.items()})
            return output.getvalue()
            
        elif format == ExportFormat.XML:
            root = ET.Element("users")
            for user in users:
                user_elem = ET.SubElement(root, "user")
                for key, value in user.items():
                    elem = ET.SubElement(user_elem, key)
                    elem.text = str(value)
            return ET.tostring(root, encoding='unicode', method='xml') 