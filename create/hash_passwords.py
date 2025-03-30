import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

if __name__ == "__main__":
    admin_password = "123a"
    user_password = "123u"

    admin_password_hash = hash_password(admin_password)
    user_password_hash = hash_password(user_password)

    print(f"Хэш администратора: {admin_password_hash}")
    print(f"Хэш пользователя: {user_password_hash}")
