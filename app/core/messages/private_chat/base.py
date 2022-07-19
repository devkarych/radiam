from aiogram.utils.markdown import hbold as bold, hlink as link


def welcome(user_firstname: str) -> str:
    """
    :param user_firstname:
    :return: welcome message to user
    """

    return bold(f'Hello, {user_firstname}!') + \
           f"\n\nThis is {link(title='Radiam', url='https://github.com/devkarych/radiam')}." \
           f"\nAuthor: @karych.\n\n" \
           f"<i>Send a url to chat and I will load file from target platform. Now, supports only YouTube.</i>"


load_error = "<b>File can't be loaded.</b>\nInvalid url or something went wrong."
loading_started = "Loading started!"
