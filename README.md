# Covid19_Severity_Misinformation
This is the data and code repository for our 2020 preprint "Drink bleach or do what now? CoSevMis: A dataset for severity-informed decision making in the presence of COVID19 misinformation", where we explore how severe or risky COVID19 fake news are in the health-related decision making process of the audience. To this end, we release a novel benchmark dataset for risk-aware health misinformation detection, related to the 2019 coronavirus pandemic. Social media posts (Twitter) are annotated based on the likelihood of health behavioral changes and the corresponding risks from following unreliable advice found online.

If you find this dataset, code or results useful, please cite us using the following bibTex:
```
@article{Dharawat2020covid,
  title={Adapting Sequence to Sequence models for Text Normalization in Social Media},
  author={Dharawat, Arkin and Lourentzou, Ismini and Morales, Alex and Zhai, ChengXiang},
  journal={preprint},
  year={2020}
  }
```

#### Notes
Code and data will be released very soon!

### Requirements
- python 3.7.5
- torch==1.3.1
- flair==0.5 
- scikit-learn==0.21.2
- tensorflow-gpu==2.2.0 / tensorflow==2.2.0
- keras==2.4.3
- pandas==1.0.0
- tweet-preprocessor==0.6.0

#### Download the Covid-Twitter-Bert tensorflow model and convert it to pytorch
```bash
curl -O https://crowdbreaks-public.s3.eu-central-1.amazonaws.com/models/covid-twitter-bert/v1/checkpoint_submodel/covid-twitter-bert-v1.tar.gz
tar -zxvf covid-twitter-bert-v1.tar.gz
mv covid-twitter-bert-v1 covid-twitter-bert
rm covid-twitter-bert-v1.tar.gz
python3 convert_tf_pt.py
mv covid-twitter-bert/bert_config.json covid-twitter-bert/config.json
```
