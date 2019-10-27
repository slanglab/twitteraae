from __future__ import division
import numpy as np
import sys,os

vocabfile = "../model/model_vocab.txt"
modelfile = "../model/model_count_table.txt"

K=0; wordprobs=None; w2num=None

def load_model():
    """Idempotent"""
    global vocab,w2num,N_wk,N_k,wordprobs,N_w,K, modelfile,vocabfile
    if wordprobs is not None:
        # assume already loaded
        return

    N_wk = np.loadtxt(modelfile)
    N_w = N_wk.sum(1)
    N_k = N_wk.sum(0)
    K = len(N_k)
    wordprobs = (N_wk + 1) / N_k

    vocab = [L.split("\t")[-1].strip().decode("utf-8") for L in open(vocabfile)]
    w2num = {w:i for i,w in enumerate(vocab)}
    assert len(vocab) == N_wk.shape[0]

def infer_cvb0(invocab_tokens, alpha, numpasses):
    global K,wordprobs,w2num
    doclen = len(invocab_tokens)

    # initialize with likelihoods
    Qs = np.zeros((doclen, K))
    for i in xrange(doclen):
        w = invocab_tokens[i]
        Qs[i,:] = wordprobs[w2num[w],:]
        Qs[i,:] /= Qs[i,:].sum()
    lik = Qs.copy()  # pertoken normalized but proportionally the same for inference

    Q_k = Qs.sum(0)
    for itr in xrange(1,numpasses):
        # print "cvb0 iter", itr
        for i in xrange(doclen):
            Q_k -= Qs[i,:]
            Qs[i,:] = lik[i,:] * (Q_k + alpha)
            Qs[i,:] /= Qs[i,:].sum()
            Q_k += Qs[i,:]

    Q_k /= Q_k.sum()
    return Q_k

def predict(tokens, alpha=1, numpasses=5, thresh1=1, thresh2=0.2):
    if len(tokens)>0:
        assert isinstance(tokens[0], unicode)
    invocab_tokens = [w.lower() for w in tokens if w.lower() in w2num]
    # check that at least xx tokens are in vocabulary
    if len(invocab_tokens) < thresh1:
        return None  
    # check that at least yy% of tokens are in vocabulary
    elif len(invocab_tokens) / len(tokens) < thresh2:
        return None
    else:
        posterior = infer_cvb0(invocab_tokens, alpha=alpha, numpasses=numpasses)
        return posterior
