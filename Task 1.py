import random as ra
import string as st

def generate_password():
    upperletters = st.ascii_uppercase
    lowerletters = st.ascii_lowercase
    digits = st.digits
    punctuation_sign = '?,!,@,#,$,&'

    upperletters1 = ra.choices(upperletters)
    lowerletters1 = ra.choices(lowerletters)
    digits1 = ra.choices(digits)
    punctuation1 =  ra.choices(punctuation_sign)

    all_chars = upperletters1 + lowerletters1 + digits1 + punctuation1
    remaining_chars = ''.join(ra.choice(st.ascii_letters + st.digits + st.punctuation) for _ in range(5))
    password = ''.join(ra.sample(str(all_chars) + remaining_chars, 9))

    return password
if __name__ == "__main__":
    print("generated password:", generate_password())