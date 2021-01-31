# Covid-HeRA: Health_Severity_Misinformation 
This is the data and code repository for our 2020 preprint **"Drink bleach or do what now? Covid-HeRA: A dataset for health risk assessment and severity-informed decision making in the presence of COVID19 misinformation"**, where we explore how severe or risky COVID19 fake news are in the health-related decision making process of the audience. To this end, we release a novel benchmark dataset for risk-aware health misinformation detection, related to the 2019 coronavirus pandemic. Social media posts (Twitter) are annotated based on the perceived likelihood of health behavioral changes and the perceived corresponding risks from following unreliable advice found online.

- [Preprint](https://arxiv.org/abs/2010.08743) 
- [Poster](https://uofi.app.box.com/v/CovidHeRAmisinformation) presented at NLP-COVID19 Workshop @ ACL 2020


If you find this dataset, code or results useful, please cite us using the following bibTex:
```
@misc{dharawat2020drink,
      title={Drink bleach or do what now? Covid-HeRA: A dataset for risk-informed health decision making in the presence of COVID19 misinformation}, 
      author={Arkin Dharawat and Ismini Lourentzou and Alex Morales and ChengXiang Zhai},
      year={2020},
      eprint={2010.08743},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

#### Notes
To download and pre-process the data, follow these [instructions](https://github.com/TIMAN-group/covid19_misinformation/blob/master/data/README.md)

### Requirements
- python 3.7.5
- torch==1.3.1
- flair==0.5 
- scikit-learn==0.21.2
- tensorflow-gpu==2.2.0 / tensorflow==2.2.0
- keras==2.4.3
- pandas==1.0.0
- tweet-preprocessor==0.6.0

### Labels
{0: Real News/Claims, 1: Not severe, 2: Possibly severe, 3: Highly severe, 4: Refutes/Rebuts}
