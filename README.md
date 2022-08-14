# Algorithmic Trading Workshop

In this workshop, participants will learn how to load and store financial data on AWS from AWS Data Exchange and other external data sources and how to build and backtest algorithmic trading strategies with Amazon SageMaker that use technical indicators and advanced machine learning models.

![chart](assets/chart.png)

_Time Commitment Expectation: This workshop was created to be completed in approximately 1h 30 min._

## Regions

This workshop has been tested in **us-east-1**.

## Considerations for Each Role
As the team lead on this lean team of one, you'll need to wear multiple hats.  Below are some things we'll cover from the perspective of each role:
* Data Engineer - You'll modify scripts to load external market data to AWS.
* Data Scientist - You'll need to load the data into your machine learning development environment. Once loaded, you'll understand the data, use a machine learning algorithm to train the model and do predictions.
* Trader - You will use different trading strategies based on data to maximize Profit & Loss while attributing to Risk.

## Goals

At minimum, at the end of this workshop, you will have an understanding how to load historical price data from external market data sources like AWS Data Exchange into S3. You get familiar how to store price data in S3 and expose it via Glue Data Catalog and Athena, how to backtested trading strategies using Amazon SageMaker, and how to train machine learning models that are used in trading strategies. You also get a basic understand how trading strategies using trend following and machine learning are developed with Python and can be optimized for better performance.

## Architecture

![chart](assets/arch.png)

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

<details>
<summary>  
<b>External Dependencies</b>

This package depends on and may retrieve a number of third-party software packages (such as open source packages) from third-party servers at install-time or build-time ("External Dependencies"). The External Dependencies are subject to license terms that you must accept in order to use this package. If you do not accept all of the applicable license terms, you should not use this package. We recommend that you consult your company’s open source approval policy before proceeding.
</summary>
Provided below is a list of the External Dependencies and the applicable license terms as indicated by the documentation associated with the External Dependencies as of Amazon's most recent review of such documentation.
THIS INFORMATION IS PROVIDED FOR CONVENIENCE ONLY. AMAZON DOES NOT PROMISE THAT THE LIST OR THE APPLICABLE TERMS AND CONDITIONS ARE COMPLETE, ACCURATE, OR UP-TO-DATE, AND AMAZON WILL HAVE NO LIABILITY FOR ANY INACCURACIES. YOU SHOULD CONSULT THE DOWNLOAD SITES FOR THE EXTERNAL DEPENDENCIES FOR THE MOST COMPLETE AND UP-TO-DATE LICENSING INFORMATION.
YOUR USE OF THE EXTERNAL DEPENDENCIES IS AT YOUR SOLE RISK. IN NO EVENT WILL AMAZON BE LIABLE FOR ANY DAMAGES, INCLUDING WITHOUT LIMITATION ANY DIRECT, INDIRECT, CONSEQUENTIAL, SPECIAL, INCIDENTAL, OR PUNITIVE DAMAGES (INCLUDING FOR ANY LOSS OF GOODWILL, BUSINESS INTERRUPTION, LOST PROFITS OR DATA, OR COMPUTER FAILURE OR MALFUNCTION) ARISING FROM OR RELATING TO THE EXTERNAL DEPENDENCIES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, EVEN IF AMAZON HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. THESE LIMITATIONS AND DISCLAIMERS APPLY EXCEPT TO THE EXTENT PROHIBITED BY APPLICABLE LAW.

** backtrader; version 1.9.74.123 -- https://www.backtrader.com/
</details>

## References

- Reference Architecture for Algorithmic Trading (Dec 2020): https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/algorithmic-trading-ra.pdf
- Blog Post (Feb 2021): Algorithmic Trading with SageMaker and AWS Data Exchange: https://aws.amazon.com/blogs/industries/algorithmic-trading-on-aws-with-amazon-sagemaker-and-aws-data-exchange/
- Blog Post (June 2021): How to run what-if scenarios for trading strategies with Amazon FinSpace: https://aws.amazon.com/blogs/industries/how-to-run-what-if-scenarios-for-trading-strategies-with-amazon-finspace/
- Blog Post (July 2021): Algorithmic Trading with SageMaker: https://aws.amazon.com/blogs/machine-learning/building-algorithmic-trading-strategies-with-amazon-sagemaker/
- Blog Post (Jan 2022): Backtest trading strategies with Amazon Kinesis Data Streams long-term retention and Amazon SageMaker: https://aws.amazon.com/blogs/big-data/backtest-trading-strategies-with-amazon-kinesis-data-streams-long-term-retention-and-amazon-sagemaker/
- YouTube (Dec 2020): Automated Analysis of Financial Data and Algorithmic Trading: https://www.youtube.com/watch?v=i0izMuiU12I

---

## Instructions using SageMaker Studio 

A newer version of this workshop has been developed for SageMaker Studio and is available in folder **5_SageMakerStudio**. 

1. Setup SageMaker Studio with sufficient permissions.
1. Run Jupyter Notebook: **1_Setup.ipynb**: This will setup S3 bucket, Glue Data Catalog Schema, Athena Workgroup. For SageMaker Studio, a custom kernel is built and attached.
1. Run Jupyter Notebook: **2_Load_Data.ipynb**: This will load daily stock price data into the S3 bucket.
1. Run Jupyter Notebook: **3_Backtest_Strategy.ipynb**: Backtest strategy in SageMaker Studio and find optimal parameters.

---

## Instructions using SageMaker Notebooks

## Step 0: Set up environment

1. Create a new unique S3 bucket that starts with "**algotrading-**" (e.g. "**algotrading-YYYY-MM-DD-XYZ**") that we use for storing external price data. 
1. For the base infrastructure components (SageMaker Notebook, Athena, Glue Tables), deploy the following [CloudFormation template](https://github.com/aws-samples/algorithmic-trading/raw/master/0_Setup/algo-reference.yaml). Go to [CloudFormation](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=algotrading) and upload the downloaded CF template. For the S3 bucket specify the previously created bucket name. Verify that stackName is **algotrading** before creating the stack and acknowledge that IAM changes will be made.

This step will take ca. 5 minutes.

## Step 1: Load Historical Price Data

Here are a few data source options for this workshop. The daily datasets can be downloaded and generated in a few minutes, for the intraday dataset, please plan for at least 15 mins.
1. Sample Daily EOD Stock Price Data (from public data source or AWS Data Exchange)

### Option 1a: Sample Daily EOD Stock Price Data (from public data source)

If you are not able to use AWS Data Exchange in your account, you can run instead the following Jupyter notebook that generates some sample EOD price data from a public data souce. Run all the cells in **1_Data/Load_Hist_Data_Daily_Public.ipynb**.

### Option 1b: Sample Daily EOD Stock Price Data (via AWS Data Exchange)

If you want to use AWS Data Exchange, you can download the following [dataset](https://aws.amazon.com/marketplace/pp/prodview-e2aizdzkos266#overview) for example. There are multiple options available, and we picked this for demonstration purposes. 

To download this dataset, complete a subscription request first where you provide the required information for Company Name, Name, Email Address, and Intended Use Case. Once the provider confirms the subscription, you can navigate to [AWS Data Exchange/My subscriptions/Entitled data](https://console.aws.amazon.com/dataexchange/home?#/entitled-data).
Then choose the latest revision for this subscription, select all assets, and click on **Export to Amazon S3**. In the new window select the root folder of the S3 bucket that starts with "*algotrading-data-*". Then click on **Export** and wait until your export job is completed.

In order to use this dataset for algorithmic trading, we want to standardize it to a CSV file with the following columns: **dt, sym, open, high, low, close, vol**.
Once you have successfully exported the dataset, please run the the following Jupyter notebook to format the dataset and store it in the ***hist_data_daily*** folder of your S3 bucket. Go to [Amazon SageMaker/Notebook/Notebook instances](https://console.aws.amazon.com/sagemaker/home?#/notebook-instances), then click on **Open Jupyter** for the provisioned notebook instance. Run all the cells in **1_Data/Load_Hist_Data_Daily.ipynb**.

## Step 2: Backtest a trend following strategy (or move directly to Step 3)

In this module, we backtest a trend following strategy on daily price data with Amazon SageMaker. For these notebooks, please ensure that you have daily price data loaded.

You can choose between the following trading strategies:
1. **Simple Moving Average Strategy**: **2_Strategies/Strategy SMA.ipynb**

1. **Daily Breakout Strategy**: **2_Strategies/Strategy_Breakout.ipynb**

Select the Jupyter Notebook for backtesting the strategy in the folder **2_Strategies** for your selected strategy and run it from your Amazon SageMaker Notebook instance. In the instructions, there is guidance on how to optimize the strategy.

## Step 3: Backtest a machine-learning based strategy

In this module, we backtest a machine-learning strategy with Amazon SageMaker on daily or intraday price data. Please ensure that you have daily or intraday price data loaded before running the corresponding notebooks.

Usually you will have two parts, one for training the machine learning model, and one for backtesting the strategy. You can run both notebooks or skip the training of the model as a trained model is already available in the repository:

**ML Long/Short Prediction Strategy**
* Model Training (Daily Price Data) (Optional): **3_Models/Train_Model_Forecast.ipynb**
* Strategy Backtesting (Daily Price Data): **2_Strategies/Strategy_Forecast.ipynb**

---

## Instructions using Amazon FinSpace

1. Setup Amazon FinSpace
1. Run the following notebook: **2_Strategies/Strategy_WhatIfScenarios.ipynb** in Amazon FinSpace

### Congratulations! You have completed the workshop. Don't forget to cleanup the resources if you use your own account in this workshop.