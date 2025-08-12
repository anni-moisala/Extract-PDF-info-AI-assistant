def print_test(*args, **kwargs):
    print("Positional arguments:")
    for i, arg in enumerate(args, start=1):
        print(f"  Arg {i}: {arg}")

    print("Keyword arguments:")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")
