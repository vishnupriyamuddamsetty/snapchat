import os
import cv2
import matplotlib.pyplot as plt

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.snaps_received = []

users = {}

def send_snap(sender_username):
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Error: Camera not found!")
        return

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error reading frame")
            break
        
        cv2.imshow("capture", frame)
        key = cv2.waitKey(1)

        if key == ord(' '):
            receiver = input("Enter the username of the recipient: ")
            
            if receiver not in users:
                print(f"No such user: {receiver}")
                continue

            dir_path = os.path.join(os.getcwd(), receiver, "received_snaps", sender_username)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            snap_path = os.path.join(dir_path, "snap_from_" + sender_username + ".jpg")

            if os.path.exists(snap_path):
                print("Warning: File already exists. Overwriting...")

            cv2.imwrite(snap_path, frame)
            users[receiver].snaps_received.append(snap_path)
            print(f"Snap captured and sent to {receiver}!")
            break

    cam.release()
    cv2.destroyAllWindows()

def view_snaps(username):
    dir_path = os.path.join(os.getcwd(), username, "received_snaps")
    
    if not os.path.exists(dir_path):
        print(f"No snaps directory found for user {username}!")
        return

    
    senders = [s for s in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, s))]
    
    if not senders:
        print("No snaps received.")
        return
    
    for sender in senders:
        sender_snap_dir = os.path.join(dir_path, sender)
        snaps = [snap for snap in os.listdir(sender_snap_dir) if snap.endswith('.jpg')]
        for snap in snaps:
            snap_path = os.path.join(sender_snap_dir, snap)
            img = cv2.imread(snap_path)
            if img is None:
                print(f"Error reading snap at {snap_path}!")
                continue
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.title(f"Snap from {sender}")
            plt.axis('off') 
            plt.show()
            cv2.waitKey(0)
            cv2.destroyAllWindows()


def logout():
    exit()

while True:
    print("1. Signup\n2. Login\n3. Logout")
    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        
        if username in users:
            print("Username already taken.")
            continue
        
        users[username] = User(username, password)
        dir_path = os.path.join(os.getcwd(), username, "received_snaps")
        os.makedirs(dir_path, exist_ok=True)

        print("Signup successfully completed.")

    elif choice == '2':
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        
        if username in users and users[username].password == password:
            print("Login successfully completed.")
            print("1. Send Snap\n2. View Snaps\n3. Logout")
            user_choice = input("Enter your choice: ")

            if user_choice == '1':
                send_snap(username)
            elif user_choice == '2':
                view_snaps(username)
            elif user_choice == '3':
                logout()
        else:
            print("Invalid username or password.")
