#ok so I'm writing this comment as a big TO:DO on how will settings objects act
#for now we have a "half-prototype demigod class" for handling all input regarding aligner
from Bio import Seq
class AlgorithmSettings:
    def __init__(self):
        #Pairwise aligner mode: global-default, fogsaa- inform about potential warnings from distant seqs, local-inform about possible
        self.dataset=list()
        self.algorithm_mode="global"
        self.match_score=1.0
        self.missmatch_score=-1.0
        self.gap_score=-2.0
        self.affine_gap_enabled=False
        self.gap_start_score=-2.0
        self.gap_extend_score=-1.5
        #TO:DO: write thing that converts distance into 
        self.normalisation_mode="mode"