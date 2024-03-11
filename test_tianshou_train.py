import argparse
import pprint

from tianshou_train import get_args, train_agent, watch


def test_tic_tac_toe(args: argparse.Namespace = get_args()) -> None:
    if args.watch:
        watch(args)
        return
    result, agent = train_agent(args)
    
    assert result.best_reward >= args.win_rate

    if __name__ == "__main__":
        pprint.pprint(result)
        # Let's watch its performance!
        watch(args, agent)


if __name__ == "__main__":
    test_tic_tac_toe(get_args())