import os
from utils.coco import COCO
from utils.eval_MR_multisetup import COCOeval


def validate(annFile, dt_path):
    mean_MR = []
    for id_setup in range(0, 4):
        cocoGt = COCO(annFile)
        cocoDt = cocoGt.loadRes(dt_path)
        imgIds = sorted(cocoGt.getImgIds())
        cocoEval = COCOeval(cocoGt, cocoDt, 'bbox')
        cocoEval.params.imgIds = imgIds
        cocoEval.evaluate(id_setup)
        cocoEval.accumulate()
        mean_MR.append(cocoEval.summarize_nofile(id_setup))
    return mean_MR

if __name__=='__main__':
    annType = 'bbox' #specify type here

    #initialize COCO ground truth api
    annFile = '../val_gt.json'
    main_path = '../../output/valresults/city/h/off'
    for f in sorted(os.listdir(main_path)):
        print (f)
        # initialize COCO detections api
        dt_path = os.path.join(main_path, f)
        resFile = os.path.join(dt_path,'val_dt.json')
        respath = os.path.join(dt_path,'results.txt')
        # if os.path.exists(respath):
        #     continue
        ## running evaluation
        res_file = open(respath, "w")
        for id_setup in range(0,1):
            cocoGt = COCO(annFile)
            cocoDt = cocoGt.loadRes(resFile)
            imgIds = sorted(cocoGt.getImgIds())
            cocoEval = COCOeval(cocoGt,cocoDt,annType)
            cocoEval.params.imgIds  = imgIds
            cocoEval.evaluate(id_setup)
            cocoEval.accumulate()
            cocoEval.summarize(id_setup,res_file)

        res_file.close()
