import sqlite3

def init_users():
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()

    # 50 个同学的测试数据（user_id, username, interests）
    users = [
        ("20001", "alice", "AI, Photography, Sports"),
        ("20002", "bob", "Music, AI, Travel"),
        ("20003", "charlie", "Photography, Cooking, Travel"),
        ("20004", "david", "Sports, AI, Gaming"),
        ("20005", "eva", "Music, Dance, Photography"),
        ("20006", "frank", "AI, Robotics, Sports"),
        ("20007", "grace", "Cooking, Travel, Photography"),
        ("20008", "henry", "AI, Music, Sports"),
        ("20009", "irene", "Travel, Photography, Dance"),
        ("20010", "jack", "Gaming, AI, Sports"),
        ("20011", "kate", "Music, AI, Photography"),
        ("20012", "leo", "Sports, Cooking, Travel"),
        ("20013", "mia", "AI, Dance, Photography"),
        ("20014", "nick", "Music, Travel, Sports"),
        ("20015", "olivia", "Photography, AI, Cooking"),
        ("20016", "paul", "Sports, Gaming, AI"),
        ("20017", "queen", "Travel, Photography, Music"),
        ("20018", "ryan", "AI, Robotics, Sports"),
        ("20019", "sophia", "Cooking, AI, Photography"),
        ("20020", "tom", "Music, Sports, Travel"),
        ("20021", "uma", "AI, Dance, Photography"),
        ("20022", "victor", "Sports, AI, Gaming"),
        ("20023", "wendy", "Photography, Cooking, Travel"),
        ("20024", "xavier", "AI, Music, Sports"),
        ("20025", "yara", "Travel, Photography, Dance"),
        ("20026", "zack", "Gaming, AI, Sports"),
        ("20027", "amy", "Music, AI, Photography"),
        ("20028", "brian", "Sports, Cooking, Travel"),
        ("20029", "cindy", "AI, Dance, Photography"),
        ("20030", "daniel", "Music, Travel, Sports"),
        ("20031", "ella", "Photography, AI, Cooking"),
        ("20032", "felix", "Sports, Gaming, AI"),
        ("20033", "gina", "Travel, Photography, Music"),
        ("20034", "harry", "AI, Robotics, Sports"),
        ("20035", "isabel", "Cooking, AI, Photography"),
        ("20036", "jason", "Music, Sports, Travel"),
        ("20037", "karen", "AI, Dance, Photography"),
        ("20038", "liam", "Sports, AI, Gaming"),
        ("20039", "nina", "Photography, Cooking, Travel"),
        ("20040", "oscar", "AI, Music, Sports"),
        ("20041", "peter", "Travel, Photography, Dance"),
        ("20042", "quincy", "Gaming, AI, Sports"),
        ("20043", "rose", "Music, AI, Photography"),
        ("20044", "sam", "Sports, Cooking, Travel"),
        ("20045", "tina", "AI, Dance, Photography"),
        ("20046", "ursula", "Music, Travel, Sports"),
        ("20047", "vincent", "Photography, AI, Cooking"),
        ("20048", "will", "Sports, Gaming, AI"),
        ("20049", "xena", "Travel, Photography, Music"),
        ("20050", "yuki", "AI, Robotics, Sports"),
    ]

    for user_id, username, interests in users:
        cursor.execute("INSERT INTO user_interests (user_id, username, interests) VALUES (?, ?, ?)",
                       (user_id, username, interests))

    conn.commit()
    conn.close()
    print("✅ 50 test users added!")

if __name__ == "__main__":
    init_users()
