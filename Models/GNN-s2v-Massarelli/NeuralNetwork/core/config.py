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
#  Implementation of the models based on Graph Neural Network (GNN)          #
#    and Structure2vec (s2v).                                                #
#                                                                            #
##############################################################################

import json
import os

import logging

log = logging.getLogger("s2v")


def dump_config_to_json(config, outputdir):
    """
    Dump the configuration file to json

    Args
        config: a dictionary with model configuration
        outputdir: path of the output directory
    """
    with open(os.path.join(outputdir, "config.json"), "w") as f_out:
        json.dump(config, f_out)
    return


def get_length_raw_features(features_type, max_instructions):
    """
    Determine the length_raw_features
    """
    if features_type == "none":
        return 7

    if features_type == "numerical":
        # Should be 7 (no betweenneess)
        return 7

    # if features_type == "opc":
    #     return 200

    if features_type == "asm":
        return max_instructions

    raise ValueError("Invalid features_type")


def get_bb_features_size(features_type):
    """
    Determine the bb_features_size
    """
    if features_type == "none":
        return 7

    if features_type == "numerical":
        # Should be 7 (no betweenneess)
        return 7

    # if features_type == "opc":
    #     return 200

    if features_type == "asm":
        return None

    raise ValueError("Invalid features_type")


def update_config_dataset1(config_dict, outputdir, featuresdir):
    """Config for Dataset-1."""
    inputdir = "/input/Dataset-1/"

    # Training
    config_dict["training"]["df_train_path"] = os.path.join(
        inputdir, "training_Dataset-1.csv"
    )
    config_dict["training"]["features_train_path"] = dict(
        none=os.path.join(
            featuresdir, "Dataset-1_training", "digraph_numerical_features.json"
        ),
        numerical=os.path.join(
            featuresdir, "Dataset-1_training", "digraph_numerical_features.json"
        ),
        # opc=os.path.join(
        #     featuresdir,
        #     "Dataset-1_training",
        #     "graph_func_dict_opc_200.json",
        # ),
        asm=os.path.join(
            featuresdir, "Dataset-1_training", "digraph_instructions_embeddings_200.json"
        ),
    )

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict["validation"] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-1.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-1.csv"),
        features_validation_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-1_validation", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-1_validation", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-1_validation",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-1_validation", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict["testing"] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-1.csv"),
            os.path.join(testdir, "neg_testing_Dataset-1.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-1.csv"),
            os.path.join(testdir, "pos_testing_Dataset-1.csv"),
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-1_Massarelli.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-1_Massarelli.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-1_Massarelli.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-1_Massarelli.csv"),
        ],
        features_testing_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-1_testing", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-1_testing", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-1_testing",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-1_testing", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

def update_config_dataset1(config_dict, outputdir, featuresdir):
    """Config for Dataset-1."""
    inputdir = "/input/Dataset-1/"

    # Training
    config_dict["training"]["df_train_path"] = os.path.join(
        inputdir, "training_Dataset-1.csv"
    )
    config_dict["training"]["features_train_path"] = dict(
        none=os.path.join(
            featuresdir, "Dataset-1_training", "digraph_numerical_features.json"
        ),
        numerical=os.path.join(
            featuresdir, "Dataset-1_training", "digraph_numerical_features.json"
        ),
        # opc=os.path.join(
        #     featuresdir,
        #     "Dataset-1_training",
        #     "graph_func_dict_opc_200.json",
        # ),
        asm=os.path.join(
            featuresdir, "Dataset-1_training", "digraph_instructions_embeddings_200.json"
        ),
    )

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict["validation"] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-1.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-1.csv"),
        features_validation_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-1_validation", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-1_validation", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-1_validation",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-1_validation", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict["testing"] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-1.csv"),
            os.path.join(testdir, "neg_testing_Dataset-1.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-1.csv"),
            os.path.join(testdir, "pos_testing_Dataset-1.csv"),
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-1_Massarelli.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-1_Massarelli.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-1_Massarelli.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-1_Massarelli.csv"),
        ],
        features_testing_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-1_testing", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-1_testing", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-1_testing",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-1_testing", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

def update_config_dataset2(config_dict, outputdir, featuresdir):
    """Config for Dataset-2."""
    inputdir = "/input/Dataset-2/"

    # Training
    config_dict["training"]["df_train_path"] = os.path.join(
        inputdir, "training_Dataset-2.csv"
    )
    config_dict["training"]["features_train_path"] = dict(
        none=os.path.join(
            featuresdir, "Dataset-2_training", "digraph_numerical_features.json"
        ),
        numerical=os.path.join(
            featuresdir, "Dataset-2_training", "digraph_numerical_features.json"
        ),
        # opc=os.path.join(
        #     featuresdir,
        #     "Dataset-2_training",
        #     "graph_func_dict_opc_200.json",
        # ),
        asm=os.path.join(
            featuresdir, "Dataset-2_training", "digraph_instructions_embeddings_200.json"
        ),
    )

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict["validation"] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-2.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-2.csv"),
        features_validation_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-2_validation", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-2_validation", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-2_validation",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-2_validation", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict["testing"] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-2.csv"),
            os.path.join(testdir, "neg_testing_Dataset-2.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-2.csv"),
            os.path.join(testdir, "pos_testing_Dataset-2.csv"),
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-2_Massarelli.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-2_Massarelli.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-2_Massarelli.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-2_Massarelli.csv"),
        ],
        features_testing_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-2_testing", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-2_testing", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-2_testing",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-2_testing", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

def update_config_dataset3(config_dict, outputdir, featuresdir):
    """Config for Dataset-3."""
    inputdir = "/input/Dataset-3/"

    # Training
    config_dict["training"]["df_train_path"] = os.path.join(
        inputdir, "training_Dataset-3.csv"
    )
    config_dict["training"]["features_train_path"] = dict(
        none=os.path.join(
            featuresdir, "Dataset-3_training", "digraph_numerical_features.json"
        ),
        numerical=os.path.join(
            featuresdir, "Dataset-3_training", "digraph_numerical_features.json"
        ),
        # opc=os.path.join(
        #     featuresdir,
        #     "Dataset-3_training",
        #     "graph_func_dict_opc_200.json",
        # ),
        asm=os.path.join(
            featuresdir, "Dataset-3_training", "digraph_instructions_embeddings_200.json"
        ),
    )

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict["validation"] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-3.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-3.csv"),
        features_validation_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-3_validation", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-3_validation", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-3_validation",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-3_validation", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict["testing"] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-3.csv"),
            os.path.join(testdir, "neg_testing_Dataset-3.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-3.csv"),
            os.path.join(testdir, "pos_testing_Dataset-3.csv"),
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-3_Massarelli.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-3_Massarelli.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-3_Massarelli.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-3_Massarelli.csv"),
        ],
        features_testing_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-3_testing", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-3_testing", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-3_testing",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-3_testing", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

def update_config_dataset4(config_dict, outputdir, featuresdir):
    """Config for Dataset-4."""
    inputdir = "/input/Dataset-4/"

    # Training
    config_dict["training"]["df_train_path"] = os.path.join(
        inputdir, "training_Dataset-4.csv"
    )
    config_dict["training"]["features_train_path"] = dict(
        none=os.path.join(
            featuresdir, "Dataset-4_training", "digraph_numerical_features.json"
        ),
        numerical=os.path.join(
            featuresdir, "Dataset-4_training", "digraph_numerical_features.json"
        ),
        # opc=os.path.join(
        #     featuresdir,
        #     "Dataset-4_training",
        #     "graph_func_dict_opc_200.json",
        # ),
        asm=os.path.join(
            featuresdir, "Dataset-4_training", "digraph_instructions_embeddings_200.json"
        ),
    )

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict["validation"] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-4.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-4.csv"),
        features_validation_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-4_validation", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-4_validation", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-4_validation",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-4_validation", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict["testing"] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-4.csv"),
            os.path.join(testdir, "neg_testing_Dataset-4.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-4.csv"),
            os.path.join(testdir, "pos_testing_Dataset-4.csv"),
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-4_Massarelli.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-4_Massarelli.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-4_Massarelli.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-4_Massarelli.csv"),
        ],
        features_testing_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-4_testing", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-4_testing", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-4_testing",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-4_testing", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

def update_config_dataset5(config_dict, outputdir, featuresdir):
    """Config for Dataset-5."""
    inputdir = "/input/Dataset-5/"

    # Training
    config_dict["training"]["df_train_path"] = os.path.join(
        inputdir, "training_Dataset-5.csv"
    )
    config_dict["training"]["features_train_path"] = dict(
        none=os.path.join(
            featuresdir, "Dataset-5_training", "digraph_numerical_features.json"
        ),
        numerical=os.path.join(
            featuresdir, "Dataset-5_training", "digraph_numerical_features.json"
        ),
        # opc=os.path.join(
        #     featuresdir,
        #     "Dataset-5_training",
        #     "graph_func_dict_opc_200.json",
        # ),
        asm=os.path.join(
            featuresdir, "Dataset-5_training", "digraph_instructions_embeddings_200.json"
        ),
    )

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict["validation"] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-5.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-5.csv"),
        features_validation_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-5_validation", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-5_validation", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-5_validation",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-5_validation", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict["testing"] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-5.csv"),
            os.path.join(testdir, "neg_testing_Dataset-5.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-5.csv"),
            os.path.join(testdir, "pos_testing_Dataset-5.csv"),
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-5_Massarelli.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-5_Massarelli.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-5_Massarelli.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-5_Massarelli.csv"),
        ],
        features_testing_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-5_testing", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-5_testing", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-5_testing",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-5_testing", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

def update_config_dataset6(config_dict, outputdir, featuresdir):
    """Config for Dataset-6."""
    inputdir = "/input/Dataset-6/"

    # Training
    config_dict["training"]["df_train_path"] = os.path.join(
        inputdir, "training_Dataset-6.csv"
    )
    config_dict["training"]["features_train_path"] = dict(
        none=os.path.join(
            featuresdir, "Dataset-6_training", "digraph_numerical_features.json"
        ),
        numerical=os.path.join(
            featuresdir, "Dataset-6_training", "digraph_numerical_features.json"
        ),
        # opc=os.path.join(
        #     featuresdir,
        #     "Dataset-6_training",
        #     "graph_func_dict_opc_200.json",
        # ),
        asm=os.path.join(
            featuresdir, "Dataset-6_training", "digraph_instructions_embeddings_200.json"
        ),
    )

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict["validation"] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-6.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-6.csv"),
        features_validation_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-6_validation", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-6_validation", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-6_validation",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-6_validation", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict["testing"] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-6.csv"),
            os.path.join(testdir, "neg_testing_Dataset-6.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-6.csv"),
            os.path.join(testdir, "pos_testing_Dataset-6.csv"),
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-6_Massarelli.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-6_Massarelli.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-6_Massarelli.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-6_Massarelli.csv"),
        ],
        features_testing_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-6_testing", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-6_testing", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-6_testing",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-6_testing", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

def update_config_dataset7(config_dict, outputdir, featuresdir):
    """Config for Dataset-7."""
    inputdir = "/input/Dataset-7/"

    # Training
    config_dict["training"]["df_train_path"] = os.path.join(
        inputdir, "training_Dataset-7.csv"
    )
    config_dict["training"]["features_train_path"] = dict(
        none=os.path.join(
            featuresdir, "Dataset-7_training", "digraph_numerical_features.json"
        ),
        numerical=os.path.join(
            featuresdir, "Dataset-7_training", "digraph_numerical_features.json"
        ),
        # opc=os.path.join(
        #     featuresdir,
        #     "Dataset-7_training",
        #     "graph_func_dict_opc_200.json",
        # ),
        asm=os.path.join(
            featuresdir, "Dataset-7_training", "digraph_instructions_embeddings_200.json"
        ),
    )

    # Validation
    valdir = os.path.join(inputdir, "pairs", "validation")
    config_dict["validation"] = dict(
        positive_path=os.path.join(valdir, "pos_validation_Dataset-7.csv"),
        negative_path=os.path.join(valdir, "neg_validation_Dataset-7.csv"),
        features_validation_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-7_validation", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-7_validation", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-7_validation",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-7_validation", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

    # Testing
    testdir = os.path.join(inputdir, "pairs", "testing")
    config_dict["testing"] = dict(
        full_tests_inputs=[
            os.path.join(testdir, "neg_rank_testing_Dataset-7.csv"),
            os.path.join(testdir, "neg_testing_Dataset-7.csv"),
            os.path.join(testdir, "pos_rank_testing_Dataset-7.csv"),
            os.path.join(testdir, "pos_testing_Dataset-7.csv"),
        ],
        full_tests_outputs=[
            os.path.join(outputdir, "neg_rank_testing_Dataset-7_Massarelli.csv"),
            os.path.join(outputdir, "neg_testing_Dataset-7_Massarelli.csv"),
            os.path.join(outputdir, "pos_rank_testing_Dataset-7_Massarelli.csv"),
            os.path.join(outputdir, "pos_testing_Dataset-7_Massarelli.csv"),
        ],
        features_testing_path=dict(
            none=os.path.join(
                featuresdir, "Dataset-7_testing", "digraph_numerical_features.json"
            ),
            numerical=os.path.join(
                featuresdir, "Dataset-7_testing", "digraph_numerical_features.json"
            ),
            # opc=os.path.join(
            #     featuresdir,
            #     "Dataset-7_testing",
            #     "graph_func_dict_opc_200.json",
            # ),
            asm=os.path.join(
                featuresdir, "Dataset-7_testing", "digraph_instructions_embeddings_200.json"
            ),
        ),
    )

def get_config(args):
    """The default configs."""

    config_dict = dict(
        network_type=args.network_type,
        features_type=args.features_type,
        max_num_vertices=args.max_num_vertices,
        # Dimension of each function embedding
        embedding_size=64,
        random_embeddings=args.random_embeddings,
        trainable_embeddings=args.trainable_embeddings,
        path_embedding_matrix=args.embedding_matrix,
        # bb_features_size is the size of the feature vector for each BB
        # If instruction embeddings are used, the bb_features_size is
        # automatically inferred by the embeddings matrix.
        # DO NOT CONFUSE this with the length_raw_features, which is used for
        # the padding of the placeholders X_1 and X_2.
        bb_features_size=get_bb_features_size(args.features_type),
        length_raw_features=get_length_raw_features(args.features_type, args.max_instructions),
        max_lv=2,
        T_iterations=2,
        l2_reg_lambda=0,
        rnn_depth=2,
        # 0:lstm cell; 1: GRU cell
        rnn_kind=0,
        training=dict(learning_rate=0.001, num_epochs=args.num_epochs, print_after=100),
        validation=dict(),
        testing=dict(),
        # -1: whole dataset
        batch_size=250,
        checkpoint_dir=args.checkpointdir,
        seed=11,
    )

    if args.dataset == "Dataset-1":
        update_config_dataset1(config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == "Dataset-2":
        update_config_dataset2(config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == "Dataset-3":
        update_config_dataset3(config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == "Dataset-4":
        update_config_dataset4(config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == "Dataset-5":
        update_config_dataset5(config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == "Dataset-6":
        update_config_dataset6(config_dict, args.outputdir, args.featuresdir)
    elif args.dataset == "Dataset-7":
        update_config_dataset7(config_dict, args.outputdir, args.featuresdir)

    return config_dict
