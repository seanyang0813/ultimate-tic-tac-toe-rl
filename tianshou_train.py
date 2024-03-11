import argparse
import pprint

from tianshou_uttt import get_args, train_agent, watch


def test_tic_tac_toe(args: argparse.Namespace = get_args()) -> None:
    if args.watch:
        watch(args)
        return

    result, agent = train_agent(args)
    print(result)

    if __name__ == "__main__":
        pprint.pprint(result)
        # Let's watch its performance!
       # watch(args, agent)


if __name__ == "__main__":
    test_tic_tac_toe(get_args())