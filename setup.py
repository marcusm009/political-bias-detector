import sys
import os
import tarfile

def main():
    model_name = sys.argv[1]
    extract_model(model_name)


def extract_model(model_name, checkpoint_dir='lib/checkpoints'):
    """ Extracts the model from the checkpoints folder """

    model_tar = os.path.join(checkpoint_dir, model_name) + '.tar'

    with tarfile.open(model_tar, 'r') as tar:
        tar.extractall()


if __name__ == "__main__":
    main()
