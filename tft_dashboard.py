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
    """Load data from JSON file created by your API script"""
    try:
        # Try to load real data from your API script
        with open('tft_dashboard_data.json', 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame
        matches_df = pd.DataFrame(data['matches'])
        
        # Add game mode detection (you can enhance this logic)
        matches_df['game_mode'] = 'Solo'  # Default to Solo, update as needed
        
        # Clean up trait names
        for i, row in matches_df.iterrows():
            if 'traits' in row and row['traits']:
                # Convert trait list to main traits
                main_traits = []
                for trait in row['traits']:
                    if '_' in trait:
                        trait_name = trait.split('_')[0]
                        main_traits.append(trait_name)
                matches_df.at[i, 'traits'] = main_traits
        
        print(f"✅ Loaded {len(matches_df)} games from API data")
        return matches_df
        
    except FileNotFoundError:
        print("⚠️ No API data found, using sample data")
        # Fallback to sample data if no real data available
        return load_sample_data()
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return load_sample_data()

def load_sample_data():
    """Fallback sample data for testing"""
    matches_data = [
        {'placement': 6, 'level': 8, 'gold_left': 7, 'damage': 47, 'items': ['InfinityEdge', 'GuinsoosRageblade'], 'game_mode': 'Solo', 'traits': ['Vanguard', 'BoomBots']},
        {'placement': 3, 'level': 7, 'gold_left': 0, 'damage': 122, 'items': ['SpearOfShojin', 'Morellonomicon'], 'game_mode': 'Solo', 'traits': ['Syndicate', 'Slayer']},
        {'placement': 7, 'level': 7, 'gold_left': 0, 'damage': 63, 'items': ['BlueBuff', 'GuinsoosRageblade'], 'game_mode': 'Solo', 'traits': ['Cypher', 'Bastion']},
        {'placement': 6, 'level': 7, 'gold_left': 5, 'damage': 89, 'items': ['GargoyleStoneplate', 'GuinsoosRageblade'], 'game_mode': 'Solo', 'traits': ['Vanguard', 'Bruiser']},
        {'placement': 4, 'level': 8, 'gold_left': 1, 'damage': 119, 'items': ['InfinityEdge', 'RedBuff'], 'game_mode': 'Solo', 'traits': ['Exotech', 'Bastion']},
        {'placement': 4, 'level': 8, 'gold_left': 1, 'damage': 61, 'items': ['BrambleVest', 'SpearOfShojin'], 'game_mode': 'Solo', 'traits': ['Nitro', 'Dynamo']},
        {'placement': 4, 'level': 9, 'gold_left': 0, 'damage': 60, 'items': ['WarmogsArmor', 'HextechGunblade'], 'game_mode': 'Solo', 'traits': ['AnimaSquad', 'Vanguard']},
        {'placement': 1, 'level': 8, 'gold_left': 15, 'damage': 170, 'items': ['ThiefsGloves', 'GuinsoosRageblade'], 'game_mode': 'Solo', 'traits': ['GodoftheNet', 'AnimaSquad']},
        {'placement': 7, 'level': 7, 'gold_left': 4, 'damage': 29, 'items': ['WarmogsArmor', 'ArchangelsStaff'], 'game_mode': 'Solo', 'traits': ['StreetDemon', 'Techie']},
        {'placement': 1, 'level': 8, 'gold_left': 2, 'damage': 141, 'items': ['InfinityEdge', 'GargoyleStoneplate'], 'game_mode': 'Solo', 'traits': ['GodoftheNet', 'BoomBots']},
        {'placement': 4, 'level': 9, 'gold_left': 0, 'damage': 80, 'items': ['InfinityEdge', 'Bloodthirster'], 'game_mode': 'Solo', 'traits': ['Syndicate', 'Vanguard']},
        {'placement': 7, 'level': 7, 'gold_left': 1, 'damage': 0, 'items': ['ArchangelsStaff', 'GuinsoosRageblade'], 'game_mode': 'Solo', 'traits': ['Cypher', 'Bastion']},
        {'placement': 2, 'level': 8, 'gold_left': 10, 'damage': 177, 'items': ['Morellonomicon', 'ThiefsGloves'], 'game_mode': 'Solo', 'traits': ['Exotech', 'Bastion']},
        {'placement': 6, 'level': 8, 'gold_left': 6, 'damage': 80, 'items': ['BlueBuff', 'WarmogsArmor'], 'game_mode': 'Solo', 'traits': ['Exotech', 'Bastion']},
        {'placement': 3, 'level': 9, 'gold_left': 0, 'damage': 112, 'items': ['DragonsClaw', 'GargoyleStoneplate'], 'game_mode': 'Solo', 'traits': ['AnimaSquad', 'Vanguard']},
        {'placement': 4, 'level': 8, 'gold_left': 1, 'damage': 32, 'items': ['ZekesHerald', 'InfinityEdge'], 'game_mode': 'Solo', 'traits': ['GodoftheNet', 'Cypher']},
        {'placement': 6, 'level': 8, 'gold_left': 0, 'damage': 95, 'items': ['BrambleVest', 'RunaansHurricane'], 'game_mode': 'Solo', 'traits': ['AnimaSquad', 'Exotech']},
        {'placement': 3, 'level': 9, 'gold_left': 1, 'damage': 152, 'items': ['WarmogsArmor', 'InfinityEdge'], 'game_mode': 'Solo', 'traits': ['SoulKiller', 'GoldenOx']},
        {'placement': 3, 'level': 8, 'gold_left': 0, 'damage': 137, 'items': ['WarmogsArmor', 'GargoyleStoneplate'], 'game_mode': 'Solo', 'traits': ['GodoftheNet', 'StreetDemon']},
        {'placement': 1, 'level': 9, 'gold_left': 7, 'damage': 201, 'items': ['ThiefsGloves', 'LastWhisper'], 'game_mode': 'Double Up', 'traits': ['GodoftheNet', 'StreetDemon']},
    ]
    
    return pd.DataFrame(matches_data)

def clean_trait_name(trait_name):
    """Convert trait names to readable format"""
    return trait_name.replace('_', ' ').replace('TFT14 ', '').title()

def analyze_trait_performance(df):
    """Analyze performance by main trait"""
    trait_stats = {}
    
    for _, match in df.iterrows():
        placement = match['placement']
        # Get the main trait (usually the first one or highest tier)
        if match['traits']:
            main_trait = match['traits'][0].split('_')[0] if isinstance(match['traits'][0], str) else match['traits'][0]
            
            if main_trait not in trait_stats:
                trait_stats[main_trait] = {'placements': [], 'games': 0, 'top4': 0}
            
            trait_stats[main_trait]['placements'].append(placement)
            trait_stats[main_trait]['games'] += 1
            if placement <= 4:
                trait_stats[main_trait]['top4'] += 1
    
    # Calculate rates
    for trait, stats in trait_stats.items():
        if stats['games'] > 0:
            stats['avg_placement'] = np.mean(stats['placements'])
            stats['top4_rate'] = (stats['top4'] / stats['games']) * 100
    
    return pd.DataFrame.from_dict(trait_stats, orient='index')

def clean_item_name(item_name):
    """Convert TFT_Item_ItemName to readable format"""
    return item_name.replace('TFT_Item_', '').replace('TFT4_Item_Ornn', '').replace('TFT14_', '')

def get_item_icon_url(item_name):
    """Get the official Riot Data Dragon icon URL for a TFT item"""
    # Clean the item name and map to Riot's official item IDs
    clean_name = item_name.replace(' ', '').replace("'", '').replace('-', '').lower()
    
    # Map item names to official Riot Data Dragon item IDs for TFT Set 14
    riot_item_mapping = {
        'infinityedge': 'TFT_Item_InfinityEdge.png',
        'guinsoosrageblade': 'TFT_Item_GuinsoosRageblade.png',
        'spearofshojin': 'TFT_Item_SpearOfShojin.png',
        'warmogsarmor': 'TFT_Item_WarmogsArmor.png',
        'gargoylestoneplate': 'TFT_Item_GargoyleStoneplate.png',
        'thiefsgloves': 'TFT_Item_ThiefsGloves.png',
        'redbuff': 'TFT_Item_RedBuff.png',
        'bluebuff': 'TFT_Item_BlueBuff.png',
        'runaanshurricane': 'TFT_Item_RunaansHurricane.png',
        'jeweledgauntlet': 'TFT_Item_JeweledGauntlet.png',
        'morellonomicon': 'TFT_Item_Morellonomicon.png',
        'dragonsclaw': 'TFT_Item_DragonsClaw.png',
        'bramblevest': 'TFT_Item_BrambleVest.png',
        'archangelsstaff': 'TFT_Item_ArchangelsStaff.png',
        'hextechgunblade': 'TFT_Item_HextechGunblade.png',
        'bloodthirster': 'TFT_Item_Bloodthirster.png',
        'lastwhisper': 'TFT_Item_LastWhisper.png',
        'ionicspark': 'TFT_Item_IonicSpark.png',
        'quicksilver': 'TFT_Item_Quicksilver.png',
        'zekesherald': 'TFT_Item_ZekesHerald.png',
        'titansresolve': 'TFT_Item_TitansResolve.png',
        'adaptivehelm': 'TFT_Item_AdaptiveHelm.png',
        'statikkshiv': 'TFT_Item_StatikkShiv.png',
        'rapidfirecannon': 'TFT_Item_RapidFirecannon.png',
        'giantslayer': 'TFT_Item_GiantSlayer.png',
        'deathblade': 'TFT_Item_Deathblade.png',
        'rabadonsdeathcap': 'TFT_Item_RabadonsDeathcap.png',
        'ludensecho': 'TFT_Item_LudensEcho.png',
        'sunfirecape': 'TFT_Item_SunfireCape.png',
        'thornmail': 'TFT_Item_Thornmail.png',
        'frozenheart': 'TFT_Item_FrozenHeart.png',
        'spiritvisage': 'TFT_Item_SpiritVisage.png',
        'bansheesveil': 'TFT_Item_BansheesVeil.png',
        'handofjustice': 'TFT_Item_HandOfJustice.png',
        'forceofnature': 'TFT_Item_ForceOfNature.png',
        'locketoftheironsolari': 'TFT_Item_LocketOfTheIronSolari.png',
        'redemption': 'TFT_Item_Redemption.png',
        'crownguard': 'TFT_Item_Crownguard.png',
        'sterakskage': 'TFT_Item_SteraksGage.png',
        'edgeofnight': 'TFT_Item_EdgeOfNight.png',
        'spectralcutlass': 'TFT_Item_SpectralCutlass.png',
        'unstableconcoction': 'TFT_Item_UnstableConcoction.png',
        'nightharvester': 'TFT_Item_NightHarvester.png',
        'leviathan': 'TFT_Item_Leviathan.png',
        'spectralGauntlet': 'TFT_Item_SpectralGauntlet.png',
        'powerGauntlet': 'TFT_Item_PowerGauntlet.png',
        'emptybag': 'TFT_Item_EmptyBag.png',
        # Add more items as needed
    }
    
    # Get the official Riot filename
    riot_filename = riot_item_mapping.get(clean_name, f'TFT_Item_{item_name.replace(" ", "")}.png')
    
    # Use Riot's official Data Dragon CDN
    # Latest version for TFT items
    return f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/tft-item/{riot_filename}"

def display_item_with_icon(item_name, stats):
    """Display item with icon and stats"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        try:
            st.image(get_item_icon_url(item_name), width=64)
        except:
            # Fallback if image doesn't load
            st.markdown("⚔️")
    
    with col2:
        st.markdown(f"**{item_name}**")
        st.caption(f"{stats['games']} games")
        
        # Stats with clear headers
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("**Avg Place**")
            st.markdown(f"{stats['avg_placement']:.2f}")
        with col_b:
            st.markdown("**Top 4 Rate**")
            st.markdown(f"{stats['top4_rate']:.0f}%")
        with col_c:
            st.markdown("**Top 2 Rate**")
            if 'placements' in stats:
                top2_count = sum(1 for p in stats['placements'] if p <= 2)
                top2_rate = (top2_count / stats['games']) * 100 if stats['games'] > 0 else 0
                st.markdown(f"{top2_rate:.0f}%")
            else:
                st.markdown("0%")

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

# Generate dynamic key insights based on actual data
def generate_key_insights(df, item_performance):
    """Generate dynamic insights based on actual performance data"""
    insights = []
    
    if not item_performance.empty:
        # Find worst performing frequently used item
        frequent_items = item_performance[item_performance['games'] >= 5]
        if not frequent_items.empty:
            worst_item = frequent_items.loc[frequent_items['avg_placement'].idxmax()]
            worst_name = clean_item_name(worst_item.name)
            
            # Find best performing item for comparison
            best_item = frequent_items.loc[frequent_items['avg_placement'].idxmin()]
            best_name = clean_item_name(best_item.name)
            
            if worst_item['avg_placement'] > 4.2:
                insights.append({
                    'type': 'warning',
                    'title': f'Stop Forcing {worst_name}!',
                    'message': f'Your data shows {worst_name} has poor performance ({worst_item["avg_placement"]:.2f} avg placement, {worst_item["top4_rate"]:.0f}% top 4). Focus on {best_name} instead ({best_item["avg_placement"]:.2f} avg placement, {best_item["top4_rate"]:.0f}% top 4)!'
                })
    
    # Check level performance
    if len(df) > 10:
        avg_placement = df['placement'].mean()
        top4_rate = (df['placement'] <= 4).mean() * 100
        
        if avg_placement <= 3.5:
            insights.append({
                'type': 'success',
                'title': 'Strong Performance!',
                'message': f'Excellent {avg_placement:.2f} average placement with {top4_rate:.0f}% top 4 rate. Keep up the consistency!'
            })
        elif top4_rate >= 70:
            insights.append({
                'type': 'success', 
                'title': 'Great Top 4 Consistency!',
                'message': f'Strong {top4_rate:.0f}% top 4 rate! Focus on converting more 4ths to wins.'
            })
        elif avg_placement > 4.5:
            insights.append({
                'type': 'warning',
                'title': 'Focus on Fundamentals',
                'message': f'Average placement of {avg_placement:.2f} suggests room for improvement. Focus on economy and positioning.'
            })
    
    return insights

# Load data and generate insights
df = load_data()
item_performance = analyze_item_performance(df)
trait_performance = analyze_trait_performance(df)

# Sidebar controls
st.sidebar.header("🎛️ Dashboard Controls")

# Game mode filter
game_modes = ['All', 'Solo', 'Double Up']
selected_mode = st.sidebar.selectbox("Game Mode", game_modes)

games_to_show = st.sidebar.slider("Games to Display", min_value=5, max_value=len(df), value=min(50, len(df)))
min_item_games = st.sidebar.slider("Minimum Games for Item Analysis", min_value=1, max_value=10, value=3)

# Filter data by game mode
if selected_mode != 'All':
    df_filtered = df[df['game_mode'] == selected_mode].head(games_to_show)
else:
    df_filtered = df.head(games_to_show)

# Check if we have enough data
if len(df_filtered) == 0:
    st.error(f"No {selected_mode} games found in your data!")
    st.stop()

# Update performance analysis with filtered data
item_performance = analyze_item_performance(df_filtered)
trait_performance = analyze_trait_performance(df_filtered)

# Handle case where item_performance might be empty
if not item_performance.empty and 'games' in item_performance.columns:
    item_performance_filtered = item_performance[item_performance['games'] >= min_item_games]
else:
    item_performance_filtered = pd.DataFrame()  # Empty DataFrame if no valid data

# Generate insights after functions are defined
insights = generate_key_insights(df_filtered, item_performance)

# Key Insights Alert
st.markdown("""
<div class="highlight-box">
    <h3>🚨 Key Insight: Stop Forcing Guinsoo's Rageblade!</h3>
    <p>Your data shows Guinsoo's Rageblade has poor performance (4.38 avg placement, 46% top 4). 
    Focus on Spear of Shojin instead (3.0 avg placement, 90% top 4)!</p>
</div>
""", unsafe_allow_html=True)

# Key Takeaways Section - Dynamic based on actual data
st.subheader("🎯 Key Takeaways")
col1, col2 = st.columns(2)

# Calculate actual performance metrics
avg_placement = df_filtered['placement'].mean()
top4_rate = (df_filtered['placement'] <= 4).mean() * 100
top2_rate = (df_filtered['placement'] <= 2).mean() * 100
avg_level = df_filtered['level'].mean()

with col1:
    strengths = []
    if top4_rate >= 65:
        strengths.append(f"{top4_rate:.0f}% Top 4 rate is solid for climbing")
    if avg_level >= 8:
        strengths.append(f"Good level management ({avg_level:.1f} average)")
    if top2_rate >= 20:
        strengths.append(f"Strong top 2 rate ({top2_rate:.0f}%)")
    
    if not strengths:
        strengths = ["Building a solid foundation", "Learning from each game", "Tracking performance data"]
    
    st.markdown("#### ✅ **Strengths**")
    for strength in strengths[:4]:
        st.markdown(f"- {strength}")

with col2:
    improvements = []
    
    # Find worst performing frequent items
    if not item_performance_filtered.empty:
        frequent_bad_items = item_performance_filtered[
            (item_performance_filtered['games'] >= 5) & 
            (item_performance_filtered['avg_placement'] > 4.2)
        ]
        if not frequent_bad_items.empty:
            worst_item = frequent_bad_items.loc[frequent_bad_items['avg_placement'].idxmax()]
            improvements.append(f"Reduce {clean_item_name(worst_item.name)} usage")
    
    if avg_placement > 4.5:
        improvements.append("Focus on early game economy")
    if top4_rate < 60:
        improvements.append("Work on consistent top 4 finishes")
    if avg_level < 8:
        improvements.append("Improve leveling timing")
    
    # Check for level 7 struggles
    level_7_games = df_filtered[df_filtered['level'] == 7]
    if len(level_7_games) > 3 and level_7_games['placement'].mean() > 5:
        improvements.append("Push for level 8 more often")
    
    if not improvements:
        improvements = ["Continue current strategy", "Fine-tune positioning", "Master meta comps"]
    
    st.markdown("#### ⚠️ **Areas to Improve**")
    for improvement in improvements[:4]:
        st.markdown(f"- {improvement}")

st.markdown("---")

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    top4_rate = (df_filtered['placement'] <= 4).mean() * 100
    st.metric("Top 4 Rate", f"{top4_rate:.1f}%", delta=f"{top4_rate-60:.1f}%")

with col2:
    avg_placement = df_filtered['placement'].mean()
    st.metric("Avg Placement", f"{avg_placement:.2f}", delta=f"{4.5-avg_placement:+.2f}")

with col3:
    avg_level = df_filtered['level'].mean()
    st.metric("Avg Level", f"{avg_level:.1f}", delta=f"{avg_level-7.5:+.1f}")

with col4:
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
        # Best performing items by average placement (sorted so best items are at top)
        best_items = item_performance_filtered.nsmallest(8, 'avg_placement').sort_values('avg_placement', ascending=False)
        
        # Invert the values so lower placement = longer bars
        inverted_values = 6 - best_items['avg_placement']
        
        fig_item_perf = px.bar(
            best_items.reset_index(),
            x=inverted_values,
            y='index',
            orientation='h',
            title="🏆 Best Items by Average Placement",
            color=best_items['avg_placement'].values,
            color_continuous_scale='RdYlGn_r'
        )
        fig_item_perf.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(title="Item"),
            xaxis=dict(title="Performance (Longer = Better)")
        )
        st.plotly_chart(fig_item_perf, use_container_width=True)
    
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
                display_item_with_icon(item, stats)
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
                display_item_with_icon(item, stats)
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

# Footer
st.markdown("---")
st.markdown("*Dashboard updates automatically when you run new analysis. Data refreshes with each game session.*")
