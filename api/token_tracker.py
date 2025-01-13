# api/token_tracker.py
import time
from typing import Dict, List, Any

class TokenTracker:
    def __init__(self):
        self.usage = {
            'key1': {
                'requests': 0,
                'tokens': 0,
                'last_reset': time.time(),
                'request_history': []
            },
            'key2': {
                'requests': 0,
                'tokens': 0,
                'last_reset': time.time(),
                'request_history': []
            }
        }
    
    def count_tokens(self, text: Any) -> int:
        """Count tokens (characters) in text or nested structures"""
        if isinstance(text, str):
            return len(text)
        elif isinstance(text, dict):
            return sum(self.count_tokens(v) for v in text.values())
        elif isinstance(text, (list, tuple)):
            return sum(self.count_tokens(item) for item in text)
        return 0
    
    def update_usage(self, key_index: int, tokens: int):
        """Update usage statistics for a given API key"""
        key = f'key{key_index}'
        current_time = time.time()
        
        # Clean up old requests (older than 1 minute)
        self.usage[key]['request_history'] = [
            timestamp for timestamp in self.usage[key]['request_history']
            if current_time - timestamp < 60
        ]
        
        # Add new request
        self.usage[key]['request_history'].append(current_time)
        self.usage[key]['tokens'] += tokens
        self.usage[key]['requests'] = len(self.usage[key]['request_history'])
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics"""
        return self.usage

    def check_rate_limit(self, key_index: int) -> bool:
        """Check if rate limit is exceeded for a given API key"""
        key = f'key{key_index}'
        return len(self.usage[key]['request_history']) < 60  # 60 requests per minute