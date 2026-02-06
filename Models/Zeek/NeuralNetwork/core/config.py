##############################################################################
#                                                                            #
#  Code for the USENIX Security '22 paper:                                   #
#  How Machine Learning Is Solving the Binary Function Similarity Problem.   #
#                                                                            #
#  MIT License                                                               #
#                                                                            #
#  Copyright (c) 2019-2022 Cisco Talos                                       #
#                                                                            #
#  Permission is hereby granted, free of charge, to any person obtaining     #
#  a copy of this software and associated documentation files (the           #
#  "Software"), to deal in the Software without restriction, including       #
#  without limitation the rights to use, copy, modify, merge, publish,       #
#  distribute, sublicense, and/or sell copies of the Software, and to        #
#  permit persons to whom the Software is furnished to do so, subject to     #
#  the following conditions:                                                 #
#                                                                            #
#  The above copyright notice and this permission notice shall be            #
#  included in all copies or substantial portions of the Software.           #
#                                                                            #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,           #
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF        #
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                     #
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE    #
#  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION    #
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION     #
#  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.           #
#                                                                            #
#  Zeek Neural Network                                                       #
#                                                                            #
##############################################################################

import json
import os

import logging
log = logging.getLogger('zeek')


def dump_config_to_json(config, outputdir):
    """
    Dump the configuration file to json.

    Args
        config: a dictionary with model configuration
        outputdir: path of the output directory
    """
    with open(os.path.join(outputdir, "config.json"), "w") as f_out:
        json.dump(config, f_out)


def update_config_dataset1(config_dict, outputdir):
    """Config for Dataset-1."""
    config_dict['training']['df_train_path'] = \
        "/input/Dataset-1/training_Dataset-1.csv"
    config_dict['training']['features_train_path'] = \
        "/input/Dataset-1/features/training/zeek_Dataset-1_training.json"
    config_dict['validation'] = dict(
        positive_path="/input/Dataset-1/pairs/validation/pos_validation_Dataset-1.csv",
        negative_path="/input/Dataset-1/pairs/validation/neg_validation_Dataset-1.csv",
        features_validation_path="/input/Dataset-1/features/validation/zeek_Dataset-1_validation.json"
    )
    config_dict['testing'] = dict(
        positive_path=None,
        negative_path=None,
        full_tests_inputs=[
            "/input/Dataset-1/pairs/testing/neg_rank_testing_Dataset-1.csv",
            "/input/Dataset-1/pairs/testing/neg_testing_Dataset-1.csv",
            "/input/Dataset-1/pairs/testing/pos_rank_testing_Dataset-1.csv",
            "/input/Dataset-1/pairs/testing/pos_testing_Dataset-1.csv"
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-1_Zeek.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-1_Zeek.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-1_Zeek.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-1_Zeek.csv")
        ],
        features_testing_path="/input/Dataset-1/features/testing/zeek_Dataset-1_testing.json"
    )

def update_config_dataset2(config_dict, outputdir):
    """Config for Dataset-2."""
    config_dict['training']['df_train_path'] = \
        "/input/Dataset-2/training_Dataset-2.csv"
    config_dict['training']['features_train_path'] = \
        "/input/Dataset-2/features/training/zeek_Dataset-2_training.json"
    config_dict['validation'] = dict(
        positive_path="/input/Dataset-2/pairs/validation/pos_validation_Dataset-2.csv",
        negative_path="/input/Dataset-2/pairs/validation/neg_validation_Dataset-2.csv",
        features_validation_path="/input/Dataset-2/features/validation/zeek_Dataset-2_validation.json"
    )
    config_dict['testing'] = dict(
        positive_path=None,
        negative_path=None,
        full_tests_inputs=[
            "/input/Dataset-2/pairs/testing/neg_rank_testing_Dataset-2.csv",
            "/input/Dataset-2/pairs/testing/neg_testing_Dataset-2.csv",
            "/input/Dataset-2/pairs/testing/pos_rank_testing_Dataset-2.csv",
            "/input/Dataset-2/pairs/testing/pos_testing_Dataset-2.csv"
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-2_Zeek.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-2_Zeek.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-2_Zeek.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-2_Zeek.csv")
        ],
        features_testing_path="/input/Dataset-2/features/testing/zeek_Dataset-2_testing.json"
    )

def update_config_dataset3(config_dict, outputdir):
    """Config for Dataset-3."""
    config_dict['training']['df_train_path'] = \
        "/input/Dataset-3/training_Dataset-3.csv"
    config_dict['training']['features_train_path'] = \
        "/input/Dataset-3/features/training/zeek_Dataset-3_training.json"
    config_dict['validation'] = dict(
        positive_path="/input/Dataset-3/pairs/validation/pos_validation_Dataset-3.csv",
        negative_path="/input/Dataset-3/pairs/validation/neg_validation_Dataset-3.csv",
        features_validation_path="/input/Dataset-3/features/validation/zeek_Dataset-3_validation.json"
    )
    config_dict['testing'] = dict(
        positive_path=None,
        negative_path=None,
        full_tests_inputs=[
            "/input/Dataset-3/pairs/testing/neg_rank_testing_Dataset-3.csv",
            "/input/Dataset-3/pairs/testing/neg_testing_Dataset-3.csv",
            "/input/Dataset-3/pairs/testing/pos_rank_testing_Dataset-3.csv",
            "/input/Dataset-3/pairs/testing/pos_testing_Dataset-3.csv"
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-3_Zeek.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-3_Zeek.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-3_Zeek.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-3_Zeek.csv")
        ],
        features_testing_path="/input/Dataset-3/features/testing/zeek_Dataset-3_testing.json"
    )

def update_config_dataset4(config_dict, outputdir):
    """Config for Dataset-4."""
    config_dict['training']['df_train_path'] = \
        "/input/Dataset-4/training_Dataset-4.csv"
    config_dict['training']['features_train_path'] = \
        "/input/Dataset-4/features/training/zeek_Dataset-4_training.json"
    config_dict['validation'] = dict(
        positive_path="/input/Dataset-4/pairs/validation/pos_validation_Dataset-4.csv",
        negative_path="/input/Dataset-4/pairs/validation/neg_validation_Dataset-4.csv",
        features_validation_path="/input/Dataset-4/features/validation/zeek_Dataset-4_validation.json"
    )
    config_dict['testing'] = dict(
        positive_path=None,
        negative_path=None,
        full_tests_inputs=[
            "/input/Dataset-4/pairs/testing/neg_rank_testing_Dataset-4.csv",
            "/input/Dataset-4/pairs/testing/neg_testing_Dataset-4.csv",
            "/input/Dataset-4/pairs/testing/pos_rank_testing_Dataset-4.csv",
            "/input/Dataset-4/pairs/testing/pos_testing_Dataset-4.csv"
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-4_Zeek.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-4_Zeek.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-4_Zeek.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-4_Zeek.csv")
        ],
        features_testing_path="/input/Dataset-4/features/testing/zeek_Dataset-4_testing.json"
    )

def update_config_dataset5(config_dict, outputdir):
    """Config for Dataset-5."""
    config_dict['training']['df_train_path'] = \
        "/input/Dataset-5/training_Dataset-5.csv"
    config_dict['training']['features_train_path'] = \
        "/input/Dataset-5/features/training/zeek_Dataset-5_training.json"
    config_dict['validation'] = dict(
        positive_path="/input/Dataset-5/pairs/validation/pos_validation_Dataset-5.csv",
        negative_path="/input/Dataset-5/pairs/validation/neg_validation_Dataset-5.csv",
        features_validation_path="/input/Dataset-5/features/validation/zeek_Dataset-5_validation.json"
    )
    config_dict['testing'] = dict(
        positive_path=None,
        negative_path=None,
        full_tests_inputs=[
            "/input/Dataset-5/pairs/testing/neg_rank_testing_Dataset-5.csv",
            "/input/Dataset-5/pairs/testing/neg_testing_Dataset-5.csv",
            "/input/Dataset-5/pairs/testing/pos_rank_testing_Dataset-5.csv",
            "/input/Dataset-5/pairs/testing/pos_testing_Dataset-5.csv"
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-5_Zeek.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-5_Zeek.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-5_Zeek.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-5_Zeek.csv")
        ],
        features_testing_path="/input/Dataset-5/features/testing/zeek_Dataset-5_testing.json"
    )

def update_config_dataset6(config_dict, outputdir):
    """Config for Dataset-6."""
    config_dict['training']['df_train_path'] = \
        "/input/Dataset-6/training_Dataset-6.csv"
    config_dict['training']['features_train_path'] = \
        "/input/Dataset-6/features/training/zeek_Dataset-6_training.json"
    config_dict['validation'] = dict(
        positive_path="/input/Dataset-6/pairs/validation/pos_validation_Dataset-6.csv",
        negative_path="/input/Dataset-6/pairs/validation/neg_validation_Dataset-6.csv",
        features_validation_path="/input/Dataset-6/features/validation/zeek_Dataset-6_validation.json"
    )
    config_dict['testing'] = dict(
        positive_path=None,
        negative_path=None,
        full_tests_inputs=[
            "/input/Dataset-6/pairs/testing/neg_rank_testing_Dataset-6.csv",
            "/input/Dataset-6/pairs/testing/neg_testing_Dataset-6.csv",
            "/input/Dataset-6/pairs/testing/pos_rank_testing_Dataset-6.csv",
            "/input/Dataset-6/pairs/testing/pos_testing_Dataset-6.csv"
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-6_Zeek.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-6_Zeek.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-6_Zeek.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-6_Zeek.csv")
        ],
        features_testing_path="/input/Dataset-6/features/testing/zeek_Dataset-6_testing.json"
    )

def update_config_dataset7(config_dict, outputdir):
    """Config for Dataset-7."""
    config_dict['training']['df_train_path'] = \
        "/input/Dataset-7/training_Dataset-7.csv"
    config_dict['training']['features_train_path'] = \
        "/input/Dataset-7/features/training/zeek_Dataset-7_training.json"
    config_dict['validation'] = dict(
        positive_path="/input/Dataset-7/pairs/validation/pos_validation_Dataset-7.csv",
        negative_path="/input/Dataset-7/pairs/validation/neg_validation_Dataset-7.csv",
        features_validation_path="/input/Dataset-7/features/validation/zeek_Dataset-7_validation.json"
    )
    config_dict['testing'] = dict(
        positive_path=None,
        negative_path=None,
        full_tests_inputs=[
            "/input/Dataset-7/pairs/testing/neg_rank_testing_Dataset-7.csv",
            "/input/Dataset-7/pairs/testing/neg_testing_Dataset-7.csv",
            "/input/Dataset-7/pairs/testing/pos_rank_testing_Dataset-7.csv",
            "/input/Dataset-7/pairs/testing/pos_testing_Dataset-7.csv"
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-7_Zeek.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-7_Zeek.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-7_Zeek.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-7_Zeek.csv")
        ],
        features_testing_path="/input/Dataset-7/features/testing/zeek_Dataset-7_testing.json"
    )

def get_config(args):
    """The default configs."""

    config_dict = dict(
        nn_input_size=2048,
        vector_size=1024,
        l1_size=512,
        l2_size=128,
        dropout_reg=0.1,

        training=dict(
            learning_rate=0.001,
            num_epochs=args.num_epochs,
            print_after=20
        ),
        validation=dict(),
        testing=dict(),

        # -1: whole dataset
        batch_size=32,
        checkpoint_dir=args.checkpointdir,
        seed=11
    )

    if args.dataset == 'Dataset-1':
        update_config_dataset1(config_dict, args.outputdir)
    elif args.dataset == 'Dataset-2':
        update_config_dataset2(config_dict, args.outputdir)
    elif args.dataset == 'Dataset-3':
        update_config_dataset3(config_dict, args.outputdir)
    elif args.dataset == 'Dataset-4':
        update_config_dataset4(config_dict, args.outputdir)
    elif args.dataset == 'Dataset-5':
        update_config_dataset5(config_dict, args.outputdir)
    elif args.dataset == 'Dataset-6':
        update_config_dataset6(config_dict, args.outputdir)
    elif args.dataset == 'Dataset-7':
        update_config_dataset7(config_dict, args.outputdir)
    return config_dict
