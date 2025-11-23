
user_languages = {}
all_users = set()
broadcast_stats = {
    'total_sent': 0,
    'total_failed': 0,
    'last_broadcast': None
}

def set_user_language(user_id: int, language: str):
    user_languages[user_id] = language
    all_users.add(user_id)

def get_user_language(user_id: int) -> str:
    return user_languages.get(user_id, None)

def add_user(user_id: int):
    all_users.add(user_id)

def get_all_users() -> set:
    return all_users

def get_users_count() -> int:
    return len(all_users)

def update_broadcast_stats(sent: int, failed: int):
    broadcast_stats['total_sent'] += sent
    broadcast_stats['total_failed'] += failed
    from datetime import datetime
    broadcast_stats['last_broadcast'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_broadcast_stats() -> dict:
    return broadcast_stats
