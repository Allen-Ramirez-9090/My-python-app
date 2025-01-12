import streamlit as st
import pandas as pd
import scipy.stats
import time

# These are stateful variables which are preserved as Streamlit reruns this script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

# Header for the app
st.header('Tossing a Coin')

# Line chart initialization
chart = st.line_chart([0.5])

# Function to simulate the coin tosses
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    # Loop through the outcomes of the trials
    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])  # Update the chart with the running mean
        time.sleep(0.05)  # Small delay to show the progress on the chart

    return mean

# Slider to choose the number of trials
number_of_trials = st.slider('Number of trials?', 1, 1000, 10)

# Button to start the experiment
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials.')
    
    # Increment experiment number
    st.session_state['experiment_no'] += 1

    # Run the coin toss simulation
    mean = toss_coin(number_of_trials)

    # Append the results to the dataframe
    st.session_state['df_experiment_results'] = pd.concat([ 
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iterations', 'mean'])
        ],
        axis=0
    )

    # Reset the index of the dataframe
    st.session_state['df_experiment_results'] = \
        st.session_state['df_experiment_results'].reset_index(drop=True)

# Display the dataframe with results
st.write(st.session_state['df_experiment_results'])
