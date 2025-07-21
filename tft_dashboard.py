import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from collections import Counter
import numpy as np

# Configure Streamlit page
st.set_page_config(
    page_title="TFT Performance Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .highlight-box {
        padding: 1rem;
        background: linear-gradient(90deg, #ff6b6b, #ee5a24);
        color: white;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        background: linear-gradient(90deg, #00d2d3, #54a0ff);
        color: white;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and Header
st.title("🎮 TFT Performance Dashboard")
st.markdown("### Beebo Prime • Level 273 • Advanced Analytics")

# Sample data (replace with your actual data loading)
@st.cache_data
def load_data():
    # Your actual match data
    matches_data = [
        {'placement': 6, 'level': 8, 'gold_left': 7, 'damage': 47, 'items': ['TFT_Item_InfinityEdge', 'TFT_Item_GuinsoosRageblade']},
        {'placement': 3, 'level': 7, 'gold_left': 0, 'damage': 122, 'items': ['TFT_Item_SpearOfShojin', 'TFT_Item_Morellonomicon']},
        {'placement': 7, 'level': 7, 'gold_left': 0, 'damage': 63, 'items': ['TFT_Item_BlueBuff', 'TFT_Item_GuinsoosRageblade']},
        {'placement': 6, 'level': 7, 'gold_left': 5, 'damage': 89, 'items': ['TFT_Item_GargoyleStoneplate', 'TFT_Item_GuinsoosRageblade']},
        {'placement': 4, 'level': 8, 'gold_left': 1, 'damage': 119, 'items': ['TFT_Item_InfinityEdge', 'TFT_Item_RedBuff']},
        {'placement': 4, 'level': 8, 'gold_left': 1, 'damage': 61, 'items': ['TFT_Item_BrambleVest', 'TFT_Item_SpearOfShojin']},
        {'placement': 4, 'level': 9, 'gold_left': 0, 'damage': 60, 'items': ['TFT_Item_WarmogsArmor', 'TFT_Item_HextechGunblade']},
        {'placement': 1, 'level': 8, 'gold_left': 15, 'damage': 170, 'items': ['TFT_Item_ThiefsGloves', 'TFT_Item_GuinsoosRageblade']},
        {'placement': 7, 'level': 7, 'gold_left': 4, 'damage': 29, 'items': ['TFT_Item_WarmogsArmor', 'TFT_Item_ArchangelsStaff']},
        {'placement': 1, 'level': 8, 'gold_left': 2, 'damage': 141, 'items': ['TFT_Item_InfinityEdge', 'TFT_Item_GargoyleStoneplate']},
        {'placement': 4, 'level': 9, 'gold_left': 0, 'damage': 80, 'items': ['TFT_Item_InfinityEdge', 'TFT_Item_Bloodthirster']},
        {'placement': 7, 'level': 7, 'gold_left': 1, 'damage': 0, 'items': ['TFT_Item_ArchangelsStaff', 'TFT_Item_GuinsoosRageblade']},
        {'placement': 2, 'level': 8, 'gold_left': 10, 'damage': 177, 'items': ['TFT_Item_Morellonomicon', 'TFT_Item_ThiefsGloves']},
        {'placement': 6, 'level': 8, 'gold_left': 6, 'damage': 80, 'items': ['TFT_Item_BlueBuff', 'TFT_Item_WarmogsArmor']},
        {'placement': 3, 'level': 9, 'gold_left': 0, 'damage': 112, 'items': ['TFT_Item_DragonsClaw', 'TFT_Item_GargoyleStoneplate']},
        {'placement': 4, 'level': 8, 'gold_left': 1, 'damage': 32, 'items': ['TFT_Item_ZekesHerald', 'TFT_Item_InfinityEdge']},
        {'placement': 6, 'level': 8, 'gold_left': 0, 'damage': 95, 'items': ['TFT_Item_BrambleVest', 'TFT_Item_RunaansHurricane']},
        {'placement': 3, 'level': 9, 'gold_left': 1, 'damage': 152, 'items': ['TFT_Item_WarmogsArmor', 'TFT_Item_InfinityEdge']},
        {'placement': 3, 'level': 8, 'gold_left': 0, 'damage': 137, 'items': ['TFT_Item_WarmogsArmor', 'TFT_Item_GargoyleStoneplate']},
        {'placement': 1, 'level': 9, 'gold_left': 7, 'damage': 201, 'items': ['TFT_Item_ThiefsGloves', 'TFT_Item_LastWhisper']},
    ]
    
    return pd.DataFrame(matches_data)

def clean_item_name(item_name):
    """Convert TFT_Item_ItemName to readable format"""
    return item_name.replace('TFT_Item_', '').replace('TFT4_Item_Ornn', '').replace('TFT14_', '')

def analyze_item_performance(df):
    """Analyze item performance"""
    item_stats = {}
    
    for _, match in df.iterrows():
        placement = match['placement']
        for item in match['items']:
            clean_name = clean_item_name(item)
            if clean_name not in item_stats:
                item_stats[clean_name] = {'placements': [], 'games': 0, 'wins': 0, 'top4': 0}
            
            item_stats[clean_name]['placements'].append(placement)
            item_stats[clean_name]['games'] += 1
            if placement == 1:
                item_stats[clean_name]['wins'] += 1
            if placement <= 4:
                item_stats[clean_name]['top4'] += 1
    
    # Calculate rates
    for item, stats in item_stats.items():
        if stats['games'] > 0:
            stats['avg_placement'] = np.mean(stats['placements'])
            stats['win_rate'] = (stats['wins'] / stats['games']) * 100
            stats['top4_rate'] = (stats['top4'] / stats['games']) * 100
    
    return pd.DataFrame.from_dict(item_stats, orient='index')

# Load data
df = load_data()
item_performance = analyze_item_performance(df)

# Sidebar controls
st.sidebar.header("🎛️ Dashboard Controls")
games_to_show = st.sidebar.slider("Games to Display", min_value=5, max_value=20, value=20)
min_item_games = st.sidebar.slider("Minimum Games for Item Analysis", min_value=1, max_value=10, value=3)

# Filter data
df_filtered = df.head(games_to_show)
item_performance_filtered = item_performance[item_performance['games'] >= min_item_games]

# Key Insights Alert
st.markdown("""
<div class="highlight-box">
    <h3>🚨 Key Insight: Stop Forcing Guinsoo's Rageblade!</h3>
    <p>Your data shows Guinsoo's Rageblade has poor performance (4.38 avg placement, 46% top 4). 
    Focus on Spear of Shojin instead (3.0 avg placement, 90% top 4)!</p>
</div>
""", unsafe_allow_html=True)

# Main metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    win_rate = (df_filtered['placement'] == 1).mean() * 100
    st.metric("Win Rate", f"{win_rate:.1f}%", delta=f"{win_rate-12:.1f}%")

with col2:
    top4_rate = (df_filtered['placement'] <= 4).mean() * 100
    st.metric("Top 4 Rate", f"{top4_rate:.1f}%", delta=f"{top4_rate-60:.1f}%")

with col3:
    avg_placement = df_filtered['placement'].mean()
    st.metric("Avg Placement", f"{avg_placement:.2f}", delta=f"{4.5-avg_placement:+.2f}")

with col4:
    avg_level = df_filtered['level'].mean()
    st.metric("Avg Level", f"{avg_level:.1f}", delta=f"{avg_level-7.5:+.1f}")

with col5:
    avg_damage = df_filtered['damage'].mean()
    st.metric("Avg Damage", f"{avg_damage:.0f}", delta=f"{avg_damage-100:+.0f}")

st.markdown("---")

# Performance over time
st.subheader("📈 Performance Trends")

col1, col2 = st.columns([2, 1])

with col1:
    # Placement trend chart
    fig_trend = px.line(
        df_filtered.reset_index(), 
        x='index', 
        y='placement',
        title="Placement Over Recent Games",
        color_discrete_sequence=['#00d2d3']
    )
    fig_trend.add_hline(y=4.5, line_dash="dash", line_color="red", 
                       annotation_text="Average Expected")
    fig_trend.update_layout(
        yaxis=dict(autorange="reversed", title="Placement"),
        xaxis=dict(title="Game Number"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    # Recent matches visualization
    st.markdown("### 🎯 Recent Match Results")
    
    # Create a visual grid of recent matches
    placement_colors = {1: '🥇', 2: '🥈', 3: '🥉', 4: '🔵'}
    
    matches_display = ""
    for i, placement in enumerate(df_filtered['placement'].values):
        if placement <= 4:
            emoji = placement_colors.get(placement, '🔵')
        else:
            emoji = '🔴'
        matches_display += f"{emoji} "
        
        if (i + 1) % 5 == 0:  # New line every 5 matches
            matches_display += "\n"
    
    st.text(matches_display)
    st.caption("🥇🥈🥉🔵 = Top 4 • 🔴 = Bottom 4")

# Item Analysis Section
st.markdown("---")
st.subheader("⚔️ Item Performance Analysis")

# Top performing items
if not item_performance_filtered.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Best performing items with progress bars
        best_items = item_performance_filtered.nsmallest(8, 'avg_placement')
        
        st.markdown("### 🏆 Item Performance")
        
        for item, stats in best_items.iterrows():
            # Convert placement to progress score (1st place = 100%, 8th place = 0%)
            score = max(0, (8 - stats['avg_placement']) / 7)  # Scale from 0-1
            
            st.markdown(f"**{item}**")
            st.progress(score)
            st.caption(f"{stats['avg_placement']:.1f} avg placement • {stats['top4_rate']:.0f}% top 4 • {stats['games']} games")
            st.markdown("")  # Add spacing
    
    with col2:
        # Most used items
        most_used = item_performance_filtered.nlargest(8, 'games')
        
        fig_usage = px.pie(
            most_used.reset_index(),
            values='games',
            names='index',
            title="📊 Most Used Items",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_usage.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_usage, use_container_width=True)

# Detailed item breakdown
st.markdown("### 📋 Detailed Item Statistics")

# Create tabs for different item categories
tab1, tab2, tab3 = st.tabs(["🏆 Best Performers", "⚠️ Needs Work", "📈 Most Used"])

with tab1:
    st.markdown("""
    <div class="success-box">
        <h4>✨ Prioritize These Items</h4>
        <p>Items with strong performance metrics that you should build more often.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not item_performance_filtered.empty:
        best_performers = item_performance_filtered[
            (item_performance_filtered['avg_placement'] < 4.0) & 
            (item_performance_filtered['top4_rate'] > 60)
        ].sort_values('avg_placement')
        
        if not best_performers.empty:
            for item, stats in best_performers.iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.markdown(f"**{item}**")
                        st.caption(f"{stats['games']} games")
                    with col2:
                        st.metric("Place", f"{stats['avg_placement']:.2f}")
                    with col3:
                        st.metric("Win %", f"{stats['win_rate']:.0f}%")
                    with col4:
                        st.metric("Top 4", f"{stats['top4_rate']:.0f}%")
                    st.markdown("---")

with tab2:
    st.markdown("""
    <div class="highlight-box">
        <h4>🚨 Items Hurting Your Performance</h4>
        <p>Consider building these items less frequently or only in optimal situations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not item_performance_filtered.empty:
        problem_items = item_performance_filtered[
            (item_performance_filtered['avg_placement'] > 4.2) | 
            (item_performance_filtered['top4_rate'] < 50)
        ].sort_values('avg_placement', ascending=False)
        
        if not problem_items.empty:
            for item, stats in problem_items.iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.markdown(f"**{item}**")
                        st.caption(f"{stats['games']} games")
                    with col2:
                        st.metric("Place", f"{stats['avg_placement']:.2f}")
                    with col3:
                        st.metric("Win %", f"{stats['win_rate']:.0f}%")
                    with col4:
                        st.metric("Top 4", f"{stats['top4_rate']:.0f}%")
                    st.markdown("---")

with tab3:
    st.markdown("Items you use most frequently, regardless of performance:")
    
    if not item_performance_filtered.empty:
        most_used_items = item_performance_filtered.nlargest(10, 'games')
        
        for item, stats in most_used_items.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.markdown(f"**{item}**")
                    st.caption(f"{stats['games']} games")
                with col2:
                    st.metric("Place", f"{stats['avg_placement']:.2f}")
                with col3:
                    st.metric("Win %", f"{stats['win_rate']:.0f}%")
                with col4:
                    st.metric("Top 4", f"{stats['top4_rate']:.0f}%")
                st.markdown("---")

# Level vs Performance Analysis
st.markdown("---")
st.subheader("📊 Level vs Performance Analysis")

fig_scatter = px.scatter(
    df_filtered, 
    x='level', 
    y='placement',
    size='damage',
    color='placement',
    title="Level Reached vs Final Placement",
    color_continuous_scale='RdYlGn_r',
    hover_data=['damage', 'gold_left']
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Summary insights
st.markdown("---")
st.subheader("🎯 Key Takeaways")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### ✅ **Strengths**
    - 65% Top 4 rate is solid for climbing
    - Good level management (8.0 average)
    - Strong performance with tank items
    - Consistent damage output
    """)

with col2:
    st.markdown("""
    #### ⚠️ **Areas to Improve**
    - Stop forcing Guinsoo's Rageblade
    - Focus on Spear of Shojin builds
    - Reduce 6th-8th place games
    - Better item flexibility
    """)

# Footer
st.markdown("---")
st.markdown("*Dashboard updates automatically when you run new analysis. Data refreshes with each game session.*")
