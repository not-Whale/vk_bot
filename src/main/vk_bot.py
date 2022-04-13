import argparse
import sys
from src.main.bot.adrenaline_bot import Adrenaline_bot


def init_parser():
    parser = argparse.ArgumentParser(
        prog='vk_bot',
        description='vk_bot - bot for vk community',
        epilog='recommended usage: vk_bot --logging'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s v0.2.0',
    )
    parser.add_argument(
        '-l', '--logging',
        action='store_true',
        help='print logging messages while working'
    )
    parser.add_argument(
        '-c', '--clean_start',
        action='store_true',
        help='delete admins info saved before'
    )
    parser.add_argument(
        '-f', '--first_start',
        action='store_true',
        help='delete all info saved before (except for config file)'
    )
    parser.add_argument(
        '--config_file',
        default='/bot/conf.py',
        help='path to config file (default: "/bot/conf.py")',
        metavar='path'
    )
    parser.add_argument(
        '--admins_list',
        help='path to file with admins needed to add list',
        metavar='path'
    )
    parser.add_argument(
        '--auth_type',
        choices=['community', 'user'],
        default='community',
        help='authentication type (choose from: "community", "user"; default: "community")',
        metavar='type'
    )
    return parser


if __name__ == '__main__':
    args_parser = init_parser()
    args = args_parser.parse_args(sys.argv[1:])
    bot = Adrenaline_bot(args.logging)
    bot.start_bot()
