#!/bin/bash

# 模型权重合并
# 先下载https://github.com/nlpxucan/WizardLM, 参考https://github.com/nlpxucan/WizardLM/issues/38


# python src/weight_diff_wizard.py recover \
#           --path_raw /platform_tech/xiajun/PLMs/llama-13b-hf \
#           --path_diff /platform_tech/xiajun/PLMs/WizardLM-13B-V1.0 \
#           --path_tuned /platform_tech/xiajun/PLMs/WizardLM-13B-recover \
#           --device "cpu"

python src/weight_diff_wizard.py recover \
          --path_raw /platform_tech/xiajun/PLMs/llama-30b-hf \
          --path_diff /platform_tech/xiajun/PLMs/WizardLM-30B-V1.0 \
          --path_tuned /platform_tech/xiajun/PLMs/WizardLM-30B-recover \
          --device "cpu"