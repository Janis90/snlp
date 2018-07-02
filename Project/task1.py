import utils


def main():
    params = utils.read_params()

    print(params)

    #utils.read_file(params["train"])

    utils.generate_suffix_changing_rules("__schielen","geschielt_")


if __name__ == "__main__":
    main()
