# import time
# import sys

# def print_with_overwrite(message):
#     sys.stdout.write("\r" + " " * 50)  # Clear the entire line
#     sys.stdout.write("\r" + message)  # Write the new message
#     sys.stdout.flush()

# print("starting", end="", flush=True)

# def a(t=10):
#     for i in range(t):
#         if i % 2 == 0:
#             print_with_overwrite(f"subhash{i}")
#         else:
#             print_with_overwrite(f"subh{i}")
#         time.sleep(1)  # Just to demonstrate, you might have some other logic here

# a()


from Nara.Extra.TempMail import tempmail


mail = tempmail.OnlyMail()

print(mail)