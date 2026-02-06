##############################################################################
#                                                                            #
#  Code for the USENIX Security '22 paper:                                   #
#  How Machine Learning Is Solving the Binary Function Similarity Problem.   #
#                                                                            #
#  Copyright (c) 2019-2022 Cisco Talos                                       #
#                                                                            #
#  This program is free software: you can redistribute it and/or modify      #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation, either version 3 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  This program is distributed in the hope that it will be useful,           #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.    #
#                                                                            #
#  SAFE Neural Network                                                       #
#                                                                            #
#  This implementation contains code from                                    #
#  https://github.com/gadiluna/SAFE licensed under GPL-3.0                   #
#                                                                            #
##############################################################################

import json
import os

import logging
log = logging.getLogger('safe')


def dump_config_to_json(config, outputdir):
    """
    Dump the configuration file to JSON

    Args
        config: a dictionary with model configuration
        outputdir: path of the output directory
    """
    with open(os.path.join(outputdir, "config.json"), "w") as f_out:
        json.dump(config, f_out)
    return


def update_config_dataset1(config_dict, outputdir, featuresdir):
    """Config for Dataset-1."""
    inputdir = "/input/Dataset-1/"

    # Training
    config_dict['training']['df_train_path'] = \
        os.path.join(inputdir, "training_Dataset-1.csv")
    config_dict['training']['features_train_path'] = \
        os.path.join(
            featuresdir, "Dataset-1_training",
            "instructions_embeddings_list_250.json")

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict['validation'] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-1.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-1.csv"),
        features_validation_path=os.path.join(
            featuresdir,
            "Dataset-1_validation",
            "instructions_embeddings_list_250.json")
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict['testing'] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-1.csv"),
            os.path.join(testdir, "neg_testing_Dataset-1.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-1.csv"),
            os.path.join(testdir, "pos_testing_Dataset-1.csv")
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-1_SAFE.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-1_SAFE.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-1_SAFE.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-1_SAFE.csv")
        ],
        features_testing_path=os.path.join(
            featuresdir,
            "Dataset-1_testing",
            "instructions_embeddings_list_250.json")
    )

def update_config_dataset2(config_dict, outputdir, featuresdir):
    """Config for Dataset-2."""
    inputdir = "/input/Dataset-2/"

    # Training
    config_dict['training']['df_train_path'] = \
        os.path.join(inputdir, "training_Dataset-2.csv")
    config_dict['training']['features_train_path'] = \
        os.path.join(
            featuresdir, "Dataset-2_training",
            "instructions_embeddings_list_250.json")

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict['validation'] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-2.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-2.csv"),
        features_validation_path=os.path.join(
            featuresdir,
            "Dataset-2_validation",
            "instructions_embeddings_list_250.json")
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict['testing'] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-2.csv"),
            os.path.join(testdir, "neg_testing_Dataset-2.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-2.csv"),
            os.path.join(testdir, "pos_testing_Dataset-2.csv")
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-2_SAFE.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-2_SAFE.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-2_SAFE.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-2_SAFE.csv")
        ],
        features_testing_path=os.path.join(
            featuresdir,
            "Dataset-2_testing",
            "instructions_embeddings_list_250.json")
    )

def update_config_dataset3(config_dict, outputdir, featuresdir):
    """Config for Dataset-3."""
    inputdir = "/input/Dataset-3/"

    # Training
    config_dict['training']['df_train_path'] = \
        os.path.join(inputdir, "training_Dataset-3.csv")
    config_dict['training']['features_train_path'] = \
        os.path.join(
            featuresdir, "Dataset-3_training",
            "instructions_embeddings_list_250.json")

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict['validation'] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-3.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-3.csv"),
        features_validation_path=os.path.join(
            featuresdir,
            "Dataset-3_validation",
            "instructions_embeddings_list_250.json")
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict['testing'] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-3.csv"),
            os.path.join(testdir, "neg_testing_Dataset-3.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-3.csv"),
            os.path.join(testdir, "pos_testing_Dataset-3.csv")
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-3_SAFE.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-3_SAFE.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-3_SAFE.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-3_SAFE.csv")
        ],
        features_testing_path=os.path.join(
            featuresdir,
            "Dataset-3_testing",
            "instructions_embeddings_list_250.json")
    )

def update_config_dataset4(config_dict, outputdir, featuresdir):
    """Config for Dataset-4."""
    inputdir = "/input/Dataset-4/"

    # Training
    config_dict['training']['df_train_path'] = \
        os.path.join(inputdir, "training_Dataset-4.csv")
    config_dict['training']['features_train_path'] = \
        os.path.join(
            featuresdir, "Dataset-4_training",
            "instructions_embeddings_list_250.json")

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict['validation'] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-4.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-4.csv"),
        features_validation_path=os.path.join(
            featuresdir,
            "Dataset-4_validation",
            "instructions_embeddings_list_250.json")
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict['testing'] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-4.csv"),
            os.path.join(testdir, "neg_testing_Dataset-4.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-4.csv"),
            os.path.join(testdir, "pos_testing_Dataset-4.csv")
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-4_SAFE.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-4_SAFE.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-4_SAFE.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-4_SAFE.csv")
        ],
        features_testing_path=os.path.join(
            featuresdir,
            "Dataset-4_testing",
            "instructions_embeddings_list_250.json")
    )

def update_config_dataset5(config_dict, outputdir, featuresdir):
    """Config for Dataset-5."""
    inputdir = "/input/Dataset-5/"

    # Training
    config_dict['training']['df_train_path'] = \
        os.path.join(inputdir, "training_Dataset-5.csv")
    config_dict['training']['features_train_path'] = \
        os.path.join(
            featuresdir, "Dataset-5_training",
            "instructions_embeddings_list_250.json")

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict['validation'] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-5.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-5.csv"),
        features_validation_path=os.path.join(
            featuresdir,
            "Dataset-5_validation",
            "instructions_embeddings_list_250.json")
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict['testing'] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-5.csv"),
            os.path.join(testdir, "neg_testing_Dataset-5.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-5.csv"),
            os.path.join(testdir, "pos_testing_Dataset-5.csv")
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-5_SAFE.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-5_SAFE.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-5_SAFE.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-5_SAFE.csv")
        ],
        features_testing_path=os.path.join(
            featuresdir,
            "Dataset-5_testing",
            "instructions_embeddings_list_250.json")
    )


def update_config_dataset6(config_dict, outputdir, featuresdir):
    """Config for Dataset-6."""
    inputdir = "/input/Dataset-6/"

    # Training
    config_dict['training']['df_train_path'] = \
        os.path.join(inputdir, "training_Dataset-6.csv")
    config_dict['training']['features_train_path'] = \
        os.path.join(
            featuresdir, "Dataset-6_training",
            "instructions_embeddings_list_250.json")

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict['validation'] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-6.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-6.csv"),
        features_validation_path=os.path.join(
            featuresdir,
            "Dataset-6_validation",
            "instructions_embeddings_list_250.json")
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict['testing'] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-6.csv"),
            os.path.join(testdir, "neg_testing_Dataset-6.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-6.csv"),
            os.path.join(testdir, "pos_testing_Dataset-6.csv")
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-6_SAFE.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-6_SAFE.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-6_SAFE.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-6_SAFE.csv")
        ],
        features_testing_path=os.path.join(
            featuresdir,
            "Dataset-6_testing",
            "instructions_embeddings_list_250.json")
    )

def update_config_dataset7(config_dict, outputdir, featuresdir):
    """Config for Dataset-7."""
    inputdir = "/input/Dataset-7/"

    # Training
    config_dict['training']['df_train_path'] = \
        os.path.join(inputdir, "training_Dataset-7.csv")
    config_dict['training']['features_train_path'] = \
        os.path.join(
            featuresdir, "Dataset-7_training",
            "instructions_embeddings_list_250.json")

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict['validation'] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-7.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-7.csv"),
        features_validation_path=os.path.join(
            featuresdir,
            "Dataset-7_validation",
            "instructions_embeddings_list_250.json")
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict['testing'] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-7.csv"),
            os.path.join(testdir, "neg_testing_Dataset-7.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-7.csv"),
            os.path.join(testdir, "pos_testing_Dataset-7.csv")
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-7_SAFE.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-7_SAFE.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-7_SAFE.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-7_SAFE.csv")
        ],
        features_testing_path=os.path.join(
            featuresdir,
            "Dataset-7_testing",
            "instructions_embeddings_list_250.json")
    )

def get_config(args):
    """The default configs."""

    config_dict = dict(
        # Dimension of each function embedding
        embedding_size=100,
        random_embeddings=args.random_embeddings,
        trainable_embeddings=args.trainable_embeddings,
        path_embedding_matrix=args.embedding_matrix,
        max_instructions=args.max_instructions,

        rnn_depth=1,
        rnn_state_size=50,
        dense_layer_size=2000,
        attention_hops=10,
        attention_depth=250,

        training=dict(
            learning_rate=0.001,
            l2_reg_lambda=0,
            num_epochs=args.num_epochs,
            print_after=100
        ),
        validation=dict(),
        testing=dict(),

        # -1: whole dataset
        batch_size=250,
        checkpoint_dir=args.checkpointdir,
        seed=11
    )

    if args.dataset == 'Dataset-1':
        update_config_dataset1(
            config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == 'Dataset-2':
        update_config_dataset2(
            config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == 'Dataset-3':
        update_config_dataset3(
            config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == 'Dataset-4':
        update_config_dataset4(
            config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == 'Dataset-5':
        update_config_dataset5(
            config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == 'Dataset-6':
        update_config_dataset6(
            config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == 'Dataset-7':
        update_config_dataset7(
            config_dict, args.outputdir, args.featuresdir)

    return config_dict
