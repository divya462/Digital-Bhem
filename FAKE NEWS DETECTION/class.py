{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "68a0802a",
   "metadata": {},
   "source": [
    "# Fake News Detector"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "34865a8e",
   "metadata": {},
   "source": [
    "## Installing Necessary Libraries"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "2a23a115",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import numpy as np\n",
    "import seaborn as sns\n",
    "import string\n",
    "import re\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.metrics import accuracy_score\n",
    "from sklearn.metrics import classification_report"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "793b507f",
   "metadata": {},
   "source": [
    "## Loading the data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "efb35954",
   "metadata": {},
   "outputs": [],
   "source": [
    "data_fake=pd.read_csv('Fake.csv')\n",
    "data_true=pd.read_csv('True.csv')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "607c382f",
   "metadata": {},
   "source": [
    "### Data Preview "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "a9a4cc2b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>title</th>\n",
       "      <th>text</th>\n",
       "      <th>subject</th>\n",
       "      <th>date</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Donald Trump Sends Out Embarrassing New Year’...</td>\n",
       "      <td>Donald Trump just couldn t wish all Americans ...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 31, 2017</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Drunk Bragging Trump Staffer Started Russian ...</td>\n",
       "      <td>House Intelligence Committee Chairman Devin Nu...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 31, 2017</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Sheriff David Clarke Becomes An Internet Joke...</td>\n",
       "      <td>On Friday, it was revealed that former Milwauk...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 30, 2017</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Trump Is So Obsessed He Even Has Obama’s Name...</td>\n",
       "      <td>On Christmas day, Donald Trump announced that ...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 29, 2017</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Pope Francis Just Called Out Donald Trump Dur...</td>\n",
       "      <td>Pope Francis used his annual Christmas Day mes...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 25, 2017</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                               title  \\\n",
       "0   Donald Trump Sends Out Embarrassing New Year’...   \n",
       "1   Drunk Bragging Trump Staffer Started Russian ...   \n",
       "2   Sheriff David Clarke Becomes An Internet Joke...   \n",
       "3   Trump Is So Obsessed He Even Has Obama’s Name...   \n",
       "4   Pope Francis Just Called Out Donald Trump Dur...   \n",
       "\n",
       "                                                text subject  \\\n",
       "0  Donald Trump just couldn t wish all Americans ...    News   \n",
       "1  House Intelligence Committee Chairman Devin Nu...    News   \n",
       "2  On Friday, it was revealed that former Milwauk...    News   \n",
       "3  On Christmas day, Donald Trump announced that ...    News   \n",
       "4  Pope Francis used his annual Christmas Day mes...    News   \n",
       "\n",
       "                date  \n",
       "0  December 31, 2017  \n",
       "1  December 31, 2017  \n",
       "2  December 30, 2017  \n",
       "3  December 29, 2017  \n",
       "4  December 25, 2017  "
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data_fake.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "a6203eaa",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>title</th>\n",
       "      <th>text</th>\n",
       "      <th>subject</th>\n",
       "      <th>date</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>21412</th>\n",
       "      <td>'Fully committed' NATO backs new U.S. approach...</td>\n",
       "      <td>BRUSSELS (Reuters) - NATO allies on Tuesday we...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21413</th>\n",
       "      <td>LexisNexis withdrew two products from Chinese ...</td>\n",
       "      <td>LONDON (Reuters) - LexisNexis, a provider of l...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21414</th>\n",
       "      <td>Minsk cultural hub becomes haven from authorities</td>\n",
       "      <td>MINSK (Reuters) - In the shadow of disused Sov...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21415</th>\n",
       "      <td>Vatican upbeat on possibility of Pope Francis ...</td>\n",
       "      <td>MOSCOW (Reuters) - Vatican Secretary of State ...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21416</th>\n",
       "      <td>Indonesia to buy $1.14 billion worth of Russia...</td>\n",
       "      <td>JAKARTA (Reuters) - Indonesia will buy 11 Sukh...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                   title  \\\n",
       "21412  'Fully committed' NATO backs new U.S. approach...   \n",
       "21413  LexisNexis withdrew two products from Chinese ...   \n",
       "21414  Minsk cultural hub becomes haven from authorities   \n",
       "21415  Vatican upbeat on possibility of Pope Francis ...   \n",
       "21416  Indonesia to buy $1.14 billion worth of Russia...   \n",
       "\n",
       "                                                    text    subject  \\\n",
       "21412  BRUSSELS (Reuters) - NATO allies on Tuesday we...  worldnews   \n",
       "21413  LONDON (Reuters) - LexisNexis, a provider of l...  worldnews   \n",
       "21414  MINSK (Reuters) - In the shadow of disused Sov...  worldnews   \n",
       "21415  MOSCOW (Reuters) - Vatican Secretary of State ...  worldnews   \n",
       "21416  JAKARTA (Reuters) - Indonesia will buy 11 Sukh...  worldnews   \n",
       "\n",
       "                   date  \n",
       "21412  August 22, 2017   \n",
       "21413  August 22, 2017   \n",
       "21414  August 22, 2017   \n",
       "21415  August 22, 2017   \n",
       "21416  August 22, 2017   "
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data_true.tail()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "af3041d0",
   "metadata": {},
   "outputs": [],
   "source": [
    "data_fake[\"class\"]=0\n",
    "data_true['class']=1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "30fe3918",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "((23481, 5), (21417, 5))"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data_fake.shape, data_true.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "a2332b8d",
   "metadata": {},
   "outputs": [],
   "source": [
    "data_fake_manual_testing = data_fake.tail(10)\n",
    "for i in range(23480,23470,-1):\n",
    "    data_fake.drop([i],axis = 0, inplace = True)\n",
    "\n",
    "    \n",
    "data_true_manual_testing = data_true.tail(10)\n",
    "for i in range(21416,21406,-1):\n",
    "    data_true.drop([i],axis = 0, inplace = True)\n",
    "    \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "004f6d60",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "((23471, 5), (21407, 5))"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data_fake.shape, data_true.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "cbdb2b38",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Dell\\AppData\\Local\\Temp\\ipykernel_1640\\1676563180.py:1: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  data_fake_manual_testing['class']=0\n",
      "C:\\Users\\Dell\\AppData\\Local\\Temp\\ipykernel_1640\\1676563180.py:2: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  data_true_manual_testing['class']=1\n"
     ]
    }
   ],
   "source": [
    "data_fake_manual_testing['class']=0\n",
    "data_true_manual_testing['class']=1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "15140120",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>title</th>\n",
       "      <th>text</th>\n",
       "      <th>subject</th>\n",
       "      <th>date</th>\n",
       "      <th>class</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>23471</th>\n",
       "      <td>Seven Iranians freed in the prisoner swap have...</td>\n",
       "      <td>21st Century Wire says This week, the historic...</td>\n",
       "      <td>Middle-east</td>\n",
       "      <td>January 20, 2016</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23472</th>\n",
       "      <td>#Hashtag Hell &amp; The Fake Left</td>\n",
       "      <td>By Dady Chery and Gilbert MercierAll writers ...</td>\n",
       "      <td>Middle-east</td>\n",
       "      <td>January 19, 2016</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23473</th>\n",
       "      <td>Astroturfing: Journalist Reveals Brainwashing ...</td>\n",
       "      <td>Vic Bishop Waking TimesOur reality is carefull...</td>\n",
       "      <td>Middle-east</td>\n",
       "      <td>January 19, 2016</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23474</th>\n",
       "      <td>The New American Century: An Era of Fraud</td>\n",
       "      <td>Paul Craig RobertsIn the last years of the 20t...</td>\n",
       "      <td>Middle-east</td>\n",
       "      <td>January 19, 2016</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23475</th>\n",
       "      <td>Hillary Clinton: ‘Israel First’ (and no peace ...</td>\n",
       "      <td>Robert Fantina CounterpunchAlthough the United...</td>\n",
       "      <td>Middle-east</td>\n",
       "      <td>January 18, 2016</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23476</th>\n",
       "      <td>McPain: John McCain Furious That Iran Treated ...</td>\n",
       "      <td>21st Century Wire says As 21WIRE reported earl...</td>\n",
       "      <td>Middle-east</td>\n",
       "      <td>January 16, 2016</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23477</th>\n",
       "      <td>JUSTICE? Yahoo Settles E-mail Privacy Class-ac...</td>\n",
       "      <td>21st Century Wire says It s a familiar theme. ...</td>\n",
       "      <td>Middle-east</td>\n",
       "      <td>January 16, 2016</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23478</th>\n",
       "      <td>Sunnistan: US and Allied ‘Safe Zone’ Plan to T...</td>\n",
       "      <td>Patrick Henningsen  21st Century WireRemember ...</td>\n",
       "      <td>Middle-east</td>\n",
       "      <td>January 15, 2016</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23479</th>\n",
       "      <td>How to Blow $700 Million: Al Jazeera America F...</td>\n",
       "      <td>21st Century Wire says Al Jazeera America will...</td>\n",
       "      <td>Middle-east</td>\n",
       "      <td>January 14, 2016</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23480</th>\n",
       "      <td>10 U.S. Navy Sailors Held by Iranian Military ...</td>\n",
       "      <td>21st Century Wire says As 21WIRE predicted in ...</td>\n",
       "      <td>Middle-east</td>\n",
       "      <td>January 12, 2016</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                   title  \\\n",
       "23471  Seven Iranians freed in the prisoner swap have...   \n",
       "23472                      #Hashtag Hell & The Fake Left   \n",
       "23473  Astroturfing: Journalist Reveals Brainwashing ...   \n",
       "23474          The New American Century: An Era of Fraud   \n",
       "23475  Hillary Clinton: ‘Israel First’ (and no peace ...   \n",
       "23476  McPain: John McCain Furious That Iran Treated ...   \n",
       "23477  JUSTICE? Yahoo Settles E-mail Privacy Class-ac...   \n",
       "23478  Sunnistan: US and Allied ‘Safe Zone’ Plan to T...   \n",
       "23479  How to Blow $700 Million: Al Jazeera America F...   \n",
       "23480  10 U.S. Navy Sailors Held by Iranian Military ...   \n",
       "\n",
       "                                                    text      subject  \\\n",
       "23471  21st Century Wire says This week, the historic...  Middle-east   \n",
       "23472   By Dady Chery and Gilbert MercierAll writers ...  Middle-east   \n",
       "23473  Vic Bishop Waking TimesOur reality is carefull...  Middle-east   \n",
       "23474  Paul Craig RobertsIn the last years of the 20t...  Middle-east   \n",
       "23475  Robert Fantina CounterpunchAlthough the United...  Middle-east   \n",
       "23476  21st Century Wire says As 21WIRE reported earl...  Middle-east   \n",
       "23477  21st Century Wire says It s a familiar theme. ...  Middle-east   \n",
       "23478  Patrick Henningsen  21st Century WireRemember ...  Middle-east   \n",
       "23479  21st Century Wire says Al Jazeera America will...  Middle-east   \n",
       "23480  21st Century Wire says As 21WIRE predicted in ...  Middle-east   \n",
       "\n",
       "                   date  class  \n",
       "23471  January 20, 2016      0  \n",
       "23472  January 19, 2016      0  \n",
       "23473  January 19, 2016      0  \n",
       "23474  January 19, 2016      0  \n",
       "23475  January 18, 2016      0  \n",
       "23476  January 16, 2016      0  \n",
       "23477  January 16, 2016      0  \n",
       "23478  January 15, 2016      0  \n",
       "23479  January 14, 2016      0  \n",
       "23480  January 12, 2016      0  "
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data_fake_manual_testing.head(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "ae7531db",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>title</th>\n",
       "      <th>text</th>\n",
       "      <th>subject</th>\n",
       "      <th>date</th>\n",
       "      <th>class</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>21407</th>\n",
       "      <td>Mata Pires, owner of embattled Brazil builder ...</td>\n",
       "      <td>SAO PAULO (Reuters) - Cesar Mata Pires, the ow...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21408</th>\n",
       "      <td>U.S., North Korea clash at U.N. forum over nuc...</td>\n",
       "      <td>GENEVA (Reuters) - North Korea and the United ...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21409</th>\n",
       "      <td>U.S., North Korea clash at U.N. arms forum on ...</td>\n",
       "      <td>GENEVA (Reuters) - North Korea and the United ...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21410</th>\n",
       "      <td>Headless torso could belong to submarine journ...</td>\n",
       "      <td>COPENHAGEN (Reuters) - Danish police said on T...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21411</th>\n",
       "      <td>North Korea shipments to Syria chemical arms a...</td>\n",
       "      <td>UNITED NATIONS (Reuters) - Two North Korean sh...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 21, 2017</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21412</th>\n",
       "      <td>'Fully committed' NATO backs new U.S. approach...</td>\n",
       "      <td>BRUSSELS (Reuters) - NATO allies on Tuesday we...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21413</th>\n",
       "      <td>LexisNexis withdrew two products from Chinese ...</td>\n",
       "      <td>LONDON (Reuters) - LexisNexis, a provider of l...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21414</th>\n",
       "      <td>Minsk cultural hub becomes haven from authorities</td>\n",
       "      <td>MINSK (Reuters) - In the shadow of disused Sov...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21415</th>\n",
       "      <td>Vatican upbeat on possibility of Pope Francis ...</td>\n",
       "      <td>MOSCOW (Reuters) - Vatican Secretary of State ...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21416</th>\n",
       "      <td>Indonesia to buy $1.14 billion worth of Russia...</td>\n",
       "      <td>JAKARTA (Reuters) - Indonesia will buy 11 Sukh...</td>\n",
       "      <td>worldnews</td>\n",
       "      <td>August 22, 2017</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                   title  \\\n",
       "21407  Mata Pires, owner of embattled Brazil builder ...   \n",
       "21408  U.S., North Korea clash at U.N. forum over nuc...   \n",
       "21409  U.S., North Korea clash at U.N. arms forum on ...   \n",
       "21410  Headless torso could belong to submarine journ...   \n",
       "21411  North Korea shipments to Syria chemical arms a...   \n",
       "21412  'Fully committed' NATO backs new U.S. approach...   \n",
       "21413  LexisNexis withdrew two products from Chinese ...   \n",
       "21414  Minsk cultural hub becomes haven from authorities   \n",
       "21415  Vatican upbeat on possibility of Pope Francis ...   \n",
       "21416  Indonesia to buy $1.14 billion worth of Russia...   \n",
       "\n",
       "                                                    text    subject  \\\n",
       "21407  SAO PAULO (Reuters) - Cesar Mata Pires, the ow...  worldnews   \n",
       "21408  GENEVA (Reuters) - North Korea and the United ...  worldnews   \n",
       "21409  GENEVA (Reuters) - North Korea and the United ...  worldnews   \n",
       "21410  COPENHAGEN (Reuters) - Danish police said on T...  worldnews   \n",
       "21411  UNITED NATIONS (Reuters) - Two North Korean sh...  worldnews   \n",
       "21412  BRUSSELS (Reuters) - NATO allies on Tuesday we...  worldnews   \n",
       "21413  LONDON (Reuters) - LexisNexis, a provider of l...  worldnews   \n",
       "21414  MINSK (Reuters) - In the shadow of disused Sov...  worldnews   \n",
       "21415  MOSCOW (Reuters) - Vatican Secretary of State ...  worldnews   \n",
       "21416  JAKARTA (Reuters) - Indonesia will buy 11 Sukh...  worldnews   \n",
       "\n",
       "                   date  class  \n",
       "21407  August 22, 2017       1  \n",
       "21408  August 22, 2017       1  \n",
       "21409  August 22, 2017       1  \n",
       "21410  August 22, 2017       1  \n",
       "21411  August 21, 2017       1  \n",
       "21412  August 22, 2017       1  \n",
       "21413  August 22, 2017       1  \n",
       "21414  August 22, 2017       1  \n",
       "21415  August 22, 2017       1  \n",
       "21416  August 22, 2017       1  "
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data_true_manual_testing.head(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "39dfcd6f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>title</th>\n",
       "      <th>text</th>\n",
       "      <th>subject</th>\n",
       "      <th>date</th>\n",
       "      <th>class</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Donald Trump Sends Out Embarrassing New Year’...</td>\n",
       "      <td>Donald Trump just couldn t wish all Americans ...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 31, 2017</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Drunk Bragging Trump Staffer Started Russian ...</td>\n",
       "      <td>House Intelligence Committee Chairman Devin Nu...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 31, 2017</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Sheriff David Clarke Becomes An Internet Joke...</td>\n",
       "      <td>On Friday, it was revealed that former Milwauk...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 30, 2017</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Trump Is So Obsessed He Even Has Obama’s Name...</td>\n",
       "      <td>On Christmas day, Donald Trump announced that ...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 29, 2017</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Pope Francis Just Called Out Donald Trump Dur...</td>\n",
       "      <td>Pope Francis used his annual Christmas Day mes...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 25, 2017</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>Racist Alabama Cops Brutalize Black Boy While...</td>\n",
       "      <td>The number of cases of cops brutalizing and ki...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 25, 2017</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>Fresh Off The Golf Course, Trump Lashes Out A...</td>\n",
       "      <td>Donald Trump spent a good portion of his day a...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 23, 2017</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>Trump Said Some INSANELY Racist Stuff Inside ...</td>\n",
       "      <td>In the wake of yet another court decision that...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 23, 2017</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>Former CIA Director Slams Trump Over UN Bully...</td>\n",
       "      <td>Many people have raised the alarm regarding th...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 22, 2017</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>WATCH: Brand-New Pro-Trump Ad Features So Muc...</td>\n",
       "      <td>Just when you might have thought we d get a br...</td>\n",
       "      <td>News</td>\n",
       "      <td>December 21, 2017</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                               title  \\\n",
       "0   Donald Trump Sends Out Embarrassing New Year’...   \n",
       "1   Drunk Bragging Trump Staffer Started Russian ...   \n",
       "2   Sheriff David Clarke Becomes An Internet Joke...   \n",
       "3   Trump Is So Obsessed He Even Has Obama’s Name...   \n",
       "4   Pope Francis Just Called Out Donald Trump Dur...   \n",
       "5   Racist Alabama Cops Brutalize Black Boy While...   \n",
       "6   Fresh Off The Golf Course, Trump Lashes Out A...   \n",
       "7   Trump Said Some INSANELY Racist Stuff Inside ...   \n",
       "8   Former CIA Director Slams Trump Over UN Bully...   \n",
       "9   WATCH: Brand-New Pro-Trump Ad Features So Muc...   \n",
       "\n",
       "                                                text subject  \\\n",
       "0  Donald Trump just couldn t wish all Americans ...    News   \n",
       "1  House Intelligence Committee Chairman Devin Nu...    News   \n",
       "2  On Friday, it was revealed that former Milwauk...    News   \n",
       "3  On Christmas day, Donald Trump announced that ...    News   \n",
       "4  Pope Francis used his annual Christmas Day mes...    News   \n",
       "5  The number of cases of cops brutalizing and ki...    News   \n",
       "6  Donald Trump spent a good portion of his day a...    News   \n",
       "7  In the wake of yet another court decision that...    News   \n",
       "8  Many people have raised the alarm regarding th...    News   \n",
       "9  Just when you might have thought we d get a br...    News   \n",
       "\n",
       "                date  class  \n",
       "0  December 31, 2017      0  \n",
       "1  December 31, 2017      0  \n",
       "2  December 30, 2017      0  \n",
       "3  December 29, 2017      0  \n",
       "4  December 25, 2017      0  \n",
       "5  December 25, 2017      0  \n",
       "6  December 23, 2017      0  \n",
       "7  December 23, 2017      0  \n",
       "8  December 22, 2017      0  \n",
       "9  December 21, 2017      0  "
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data_merge=pd.concat([data_fake, data_true], axis = 0)\n",
    "data_merge.head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ea1cd410",
   "metadata": {},
   "source": [
    "#### \"title\",  \"subject\" and \"date\" columns is not required for detecting the fake news, so I am going to drop the columns."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "097c2870",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['title', 'text', 'subject', 'date', 'class'], dtype='object')"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data_merge.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "3adccb7e",
   "metadata": {},
   "outputs": [],
   "source": [
    "data=data_merge.drop(['title','subject','date'], axis = 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "8fb4c981",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "text     0\n",
       "class    0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#count of missing values\n",
    "data.isnull().sum() "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0cfe0118",
   "metadata": {},
   "source": [
    "#### Randomly shuffling the dataframe "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "fe609699",
   "metadata": {},
   "outputs": [],
   "source": [
    "data = data.sample(frac = 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "c9e879eb",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>text</th>\n",
       "      <th>class</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1147</th>\n",
       "      <td>As the divisions in the nation bubble over, it...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7953</th>\n",
       "      <td>Six people are dead after a white, domestic te...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9026</th>\n",
       "      <td>WASHINGTON (Reuters) - Democrat Hillary Clinto...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>16943</th>\n",
       "      <td>ATHENS (Reuters) - Greek police said they arre...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5809</th>\n",
       "      <td>WASHINGTON/LOS ANGELES (Reuters) - U.S. Presid...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                    text  class\n",
       "1147   As the divisions in the nation bubble over, it...      0\n",
       "7953   Six people are dead after a white, domestic te...      0\n",
       "9026   WASHINGTON (Reuters) - Democrat Hillary Clinto...      1\n",
       "16943  ATHENS (Reuters) - Greek police said they arre...      1\n",
       "5809   WASHINGTON/LOS ANGELES (Reuters) - U.S. Presid...      1"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "33ddd95b",
   "metadata": {},
   "outputs": [],
   "source": [
    "data.reset_index(inplace = True)\n",
    "data.drop(['index'], axis = 1, inplace = True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "c70930a1",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['text', 'class'], dtype='object')"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "cd7a7a95",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>text</th>\n",
       "      <th>class</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>As the divisions in the nation bubble over, it...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Six people are dead after a white, domestic te...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>WASHINGTON (Reuters) - Democrat Hillary Clinto...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>ATHENS (Reuters) - Greek police said they arre...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>WASHINGTON/LOS ANGELES (Reuters) - U.S. Presid...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                text  class\n",
       "0  As the divisions in the nation bubble over, it...      0\n",
       "1  Six people are dead after a white, domestic te...      0\n",
       "2  WASHINGTON (Reuters) - Democrat Hillary Clinto...      1\n",
       "3  ATHENS (Reuters) - Greek police said they arre...      1\n",
       "4  WASHINGTON/LOS ANGELES (Reuters) - U.S. Presid...      1"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "20157149",
   "metadata": {},
   "source": [
    "## Preprocessing Text"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "56c82e01",
   "metadata": {},
   "source": [
    "#### Creating a function to convert the text in lowercase, remove the extra space, special chr., ulr and links."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "453dfdbf",
   "metadata": {},
   "outputs": [],
   "source": [
    "def wordopt(text):\n",
    "    text = text.lower()\n",
    "    text = re.sub('\\[.*?\\]','',text)\n",
    "    text = re.sub(\"\\\\W\",\" \",text)\n",
    "    text = re.sub('https?://\\S+|www\\.\\S+','',text)\n",
    "    text = re.sub('<.*?>+',b'',text)\n",
    "    text = re.sub('[%s]' % re.escape(string.punctuation),'',text)\n",
    "    text = re.sub('\\w*\\d\\w*','',text)\n",
    "    return text"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "337d9a50",
   "metadata": {},
   "outputs": [],
   "source": [
    "data['text'] = data['text'].apply(wordopt)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "46a11e07",
   "metadata": {},
   "source": [
    "#### Defining dependent and independent variable as x and y"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "39bf4b30",
   "metadata": {},
   "outputs": [],
   "source": [
    "x = data['text']\n",
    "y = data['class']"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3a9aac19",
   "metadata": {},
   "source": [
    "## Training the model"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "415c3c72",
   "metadata": {},
   "source": [
    "#### Splitting the dataset into training set and testing set. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "645dd4c8",
   "metadata": {},
   "outputs": [],
   "source": [
    "x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.25)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b3169fde",
   "metadata": {},
   "source": [
    "### Extracting Features from the Text"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "97ddd784",
   "metadata": {},
   "source": [
    "#### Convert text to vectors"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "554bda26",
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "\n",
    "vectorization = TfidfVectorizer()\n",
    "xv_train = vectorization.fit_transform(x_train)\n",
    "xv_test = vectorization.transform(x_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "96cfbfc1",
   "metadata": {},
   "source": [
    "## Logistic Regression"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "id": "7d78b666",
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.linear_model import LogisticRegression"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "id": "2580b926",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "LogisticRegression()"
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "LR = LogisticRegression()\n",
    "LR.fit(xv_train, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "42070f76",
   "metadata": {},
   "outputs": [],
   "source": [
    "pred_lr = LR.predict(xv_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "id": "0f671957",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.9877896613190731"
      ]
     },
     "execution_count": 29,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "LR.score(xv_test, y_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "id": "e654e1f0",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       0.99      0.99      0.99      5834\n",
      "           1       0.99      0.99      0.99      5386\n",
      "\n",
      "    accuracy                           0.99     11220\n",
      "   macro avg       0.99      0.99      0.99     11220\n",
      "weighted avg       0.99      0.99      0.99     11220\n",
      "\n"
     ]
    }
   ],
   "source": [
    "print (classification_report(y_test, pred_lr))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cc114e19",
   "metadata": {},
   "source": [
    "## Decision Tree Classifier"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "id": "fe6e3389",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DecisionTreeClassifier()"
      ]
     },
     "execution_count": 31,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from sklearn.tree import DecisionTreeClassifier\n",
    "\n",
    "DT = DecisionTreeClassifier()\n",
    "DT.fit(xv_train, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "id": "b4bbeaa5",
   "metadata": {},
   "outputs": [],
   "source": [
    "pred_dt = DT.predict(xv_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "id": "442fa652",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.9952762923351158"
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "DT.score(xv_test, y_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "6fa1ecbf",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       0.99      0.99      0.99      5834\n",
      "           1       0.99      0.99      0.99      5386\n",
      "\n",
      "    accuracy                           0.99     11220\n",
      "   macro avg       0.99      0.99      0.99     11220\n",
      "weighted avg       0.99      0.99      0.99     11220\n",
      "\n"
     ]
    }
   ],
   "source": [
    "print (classification_report(y_test, pred_lr))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "50e62d57",
   "metadata": {},
   "source": [
    "## Gradient Boost Classifier"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "id": "cc25f83e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "GradientBoostingClassifier(random_state=0)"
      ]
     },
     "execution_count": 35,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from sklearn.ensemble import GradientBoostingClassifier\n",
    "\n",
    "GB = GradientBoostingClassifier(random_state = 0)\n",
    "GB.fit(xv_train, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "9c623e70",
   "metadata": {},
   "outputs": [],
   "source": [
    "pred_gb = GB.predict(xv_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "d72b75ab",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.9944741532976827"
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "GB.score(xv_test, y_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "id": "99d83e4a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       1.00      0.99      0.99      5834\n",
      "           1       0.99      1.00      0.99      5386\n",
      "\n",
      "    accuracy                           0.99     11220\n",
      "   macro avg       0.99      0.99      0.99     11220\n",
      "weighted avg       0.99      0.99      0.99     11220\n",
      "\n"
     ]
    }
   ],
   "source": [
    "print(classification_report(y_test, pred_gb))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "16da9186",
   "metadata": {},
   "source": [
    "## Random Forest Classifier"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "954338d0",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "RandomForestClassifier(random_state=0)"
      ]
     },
     "execution_count": 39,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from sklearn.ensemble import RandomForestClassifier\n",
    "\n",
    "RF = RandomForestClassifier(random_state = 0)\n",
    "RF.fit(xv_train, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "1fb15f46",
   "metadata": {},
   "outputs": [],
   "source": [
    "pred_rf = RF.predict(xv_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "id": "b86e8830",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.9869875222816399"
      ]
     },
     "execution_count": 41,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "RF.score(xv_test, y_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "id": "1d02b7fb",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       0.99      0.99      0.99      5834\n",
      "           1       0.99      0.98      0.99      5386\n",
      "\n",
      "    accuracy                           0.99     11220\n",
      "   macro avg       0.99      0.99      0.99     11220\n",
      "weighted avg       0.99      0.99      0.99     11220\n",
      "\n"
     ]
    }
   ],
   "source": [
    "print (classification_report(y_test, pred_rf))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "110d58d0",
   "metadata": {},
   "source": [
    "## Testing the Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "id": "6f8b0f43",
   "metadata": {},
   "outputs": [],
   "source": [
    "def output_lable(n):\n",
    "    if n==0:\n",
    "        return \"Fake News\"\n",
    "    elif n==1:\n",
    "        return \"Not A Fake News\"\n",
    "    \n",
    "def manual_testing(news):\n",
    "    testing_news = {\"text\":[news]}\n",
    "    new_def_test = pd.DataFrame(testing_news)\n",
    "    new_def_test['text'] = new_def_test[\"text\"].apply(wordopt)\n",
    "    new_x_test = new_def_test[\"text\"]\n",
    "    new_xv_test = vectorization.transform(new_x_test)\n",
    "    pred_LR = LR.predict(new_xv_test)\n",
    "    pred_DT = DT.predict(new_xv_test)\n",
    "    pred_GB = GB.predict(new_xv_test)\n",
    "    pred_RF = RF.predict(new_xv_test)\n",
    "    \n",
    "    return print(\"\\n\\nLR Predicition: {} \\nDT Prediction: {} \\nGBC Prediction: {} \\nRFC Prediction:{}\".format(output_lable(pred_LR[0]),\n",
    "                                                                                                             output_lable(pred_DT[0]),\n",
    "                                                                                                             output_lable(pred_GB[0]),\n",
    "                                                                                                             output_lable(pred_RF[0])))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1308fb1b",
   "metadata": {},
   "source": [
    "### Model Testing With Manual Entry"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "id": "cab83cc6",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Federal health officials told the AP they have not received any reports of Ebola cases at the Nevada event. A screenshot of a supposed post from the Centers for Disease Control and Prevention confirming such cases was fabricated. And there is no record of a national emergency being declared. The claims emerged after summer storm left muddy roads flooded, stranding tens of thousands of partygoers; event organizers let traffic flow out of the main road Monday afternoon. “So it was announced earlier that Burning Man was declared a national emergency because it was flooded, and so they sent in FEMA,” a woman claims in a TikTok video shared on Instagram, suggesting the development was suspicious. The AP found no record, including on federal websites and in White House announcements, of a national emergency declaration and FEMA confirmed that it was not involved in the situation. “No FEMA personnel or assets have been deployed to the Burning Man festival and there are no requests from local or state authorities for our assistance,” FEMA spokesperson Jeremy Edwards said in an email. The TikTok video, like other posts, goes on to relay baseless rumors of reported cases of Ebola, whose occasional outbreaks in humans primarily occur in Africa, at the festival. Some posts also shared an image made to appear that the CDC confirmed the supposed outbreak on X, the platform formerly known as Twitter. The purported X post from the agency reads, “Ebola outbreak confirmed at Black Rock City, NV. It is recommended that all Burning Man attendees remain in their dwellings until further notice. Current State of Emergency in progress.” But the CDC’s X account published no such post. “CDC has not received any reports of Ebola at the Burning Man Festival and has not issued any warnings or had any requests for assistance from the state and local health departments either,” agency spokesperson Scott Pauley said in an email. Reverse image searches further show that a graphic about Ebola used in the fictitious CDC post was published by the agency in 2016, but elements of it were changed. For example, the original graphic asks, “Recently in West Africa?” But the version used in the made-up X post asks, “Recently in Nevada?” Referencing more online rumors, Pauley also noted the CDC had not received reports of mpox, formerly known as monkeypox, or Marburg, a rare but severe hemorrhagic fever, in relation to Burning Man. A representative for the Burning Man Project organization also refuted the online claims. “Quite simply, the online rumors of transmissible illnesses in Black Rock City are unfounded and untrue,” Dominique Debucquoy-Dodley said in an email. The festival had been closed to vehicles after more than a half-inch (1.3 centimeters) of rain fell Sept. 1, causing flooding and foot-deep mud, as the AP reported. The annual gathering, which launched on a San Francisco beach in 1986, attracts nearly 80,000 artists, musicians and activists for a mix of wilderness camping and avant-garde performances\n",
      "\n",
      "\n",
      "LR Predicition: Fake News \n",
      "DT Prediction: Fake News \n",
      "GBC Prediction: Fake News \n",
      "RFC Prediction:Fake News\n"
     ]
    }
   ],
   "source": [
    "news = str(input()) \n",
    "manual_testing(news)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "id": "8b8bdbc7",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "MOSCOW (Reuters) - Russiaâ€™s former ambassador to Washington, Sergei Kislyak, said on Saturday his conversations with former White House national security adviser Michael Flynn had been transparent and focused on matters of U.S.-Russia cooperation. Kislyak ended his tenure in Washington in July but remains a key figure in ongoing U.S. investigations into Moscowâ€™s alleged meddling in the 2016 presidential election. Flynn was forced to resign in February after it became known that he had failed to disclose the content of conversations he had with Kislyak and misled U.S. Vice-President Mike Pence about their meetings. â€œWe only spoke about the most simple things ... but the communication was completely correct, calm, absolutely transparent. In any case, there were no secrets on our side,â€ Kislyak said during a panel discussion on Russian television. â€œThere are a number of issues which are important for cooperation between Russia and the United States - most of all, terrorism. And that was one of the things we discussed.â€ \n",
      "\n",
      "\n",
      "LR Predicition: Not A Fake News \n",
      "DT Prediction: Not A Fake News \n",
      "GBC Prediction: Not A Fake News \n",
      "RFC Prediction:Not A Fake News\n"
     ]
    }
   ],
   "source": [
    "news=str(input())\n",
    "manual_testing(news)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "64d52cc7",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}