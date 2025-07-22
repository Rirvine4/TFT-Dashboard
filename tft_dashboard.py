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

def clean_item_name(item_name):
    """Convert TFT_Item_ItemName to readable format"""
    # Remove various prefixes and clean up the name
    cleaned = item_name.replace('TFT_Item_', '').replace('TFT4_Item_Ornn', '').replace('TFT14_', '')
    
    # Add spaces before capital letters for readability
    import re
    spaced = re.sub(r'(?<!^)(?=[A-Z])', ' ', cleaned)
    
    return spaced

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
    }
    
    # Get the official Riot filename
    riot_filename = riot_item_mapping.get(clean_name, f'TFT_Item_{item_name.replace(" ", "")}.png')
    
    # Use Riot's official Data Dragon CDN
    return f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/tft-item/{riot_filename}"

def display_item_with_icon(item_name, stats):
    """Display item with icon and stats"""
    col1, col2 = st.columns([1, 3])
    
    # Clean the item name for display
    clean_name = clean_item_name(item_name)
    
    with col1:
        try:
            icon_url = get_item_icon_url(clean_name)
            st.image(icon_url, width=64)
        except Exception as e:
            # Fallback if image doesn't load
            st.markdown("⚔️")
    
    with col2:
        st.markdown(f"**{clean_name}**")  # Use clean name for display
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
            if 'placements' in stats and stats['placements']:
                top2_count = sum(1 for p in stats['placements'] if p <= 2)
                top2_rate = (top2_count / stats['games']) * 100 if stats['games'] > 0 else 0
                st.markdown(f"{top2_rate:.0f}%")
            else:
                st.markdown("0%")

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
        {'placement': 6, 'level': 8, 'gold_left': 7, 'damage': 47, 'items': ['InfinityEdge', 'GuinsoosRageblade'], 'game_mode': 'Solo', 'traits': ['TFT14_Vanguard_3', 'TFT14_BoomBots_2']},
        {'placement': 3, 'level': 7, 'gold_left': 0, 'damage': 122, 'items': ['SpearOfShojin', 'Morellonomicon'], 'game_mode': 'Solo', 'traits': ['TFT14_Syndicate_4', 'TFT14_Slayer_2']},
        {'placement': 7, 'level': 7, 'gold_left': 0, 'damage': 63, 'items': ['BlueBuff', 'GuinsoosRageblade'], 'game_mode': 'Solo', 'traits': ['TFT14_Cypher_2', 'TFT14_Bastion_3']},
        {'placement': 6, 'level': 7, 'gold_left': 5, 'damage': 89, 'items': ['GargoyleStoneplate', 'GuinsoosRageblade'], 'game_mode': 'Solo', 'traits': ['TFT14_Vanguard_2', 'TFT14_Bruiser_3']},
        {'placement': 4, 'level': 8, 'gold_left': 1, 'damage': 119, 'items': ['InfinityEdge', 'RedBuff'], 'game_mode': 'Solo', 'traits': ['TFT14_Exotech_4', 'TFT14_Bastion_2']},
        {'placement': 4, 'level': 8, 'gold_left': 1, 'damage': 61, 'items': ['BrambleVest', 'SpearOfShojin'], 'game_mode': 'Solo', 'traits': ['TFT14_Nitro_3', 'TFT14_Dynamo_2']},
        {'placement': 4, 'level': 9, 'gold_left': 0, 'damage': 60, 'items': ['WarmogsArmor', 'HextechGunblade'], 'game_mode': 'Solo', 'traits': ['TFT14_AnimaSquad_6', 'TFT14_Vanguard_2']},
        {'placement': 1, 'level': 8, 'gold_left': 15, 'damage': 170, 'items': ['ThiefsGloves', 'GuinsoosRageblade'], 'game_mode': 'Solo', 'traits': ['TFT14_GodoftheNet_1', 'TFT14_AnimaSquad_4']},
        {'placement': 7, 'level': 7, 'gold_left': 4, 'damage': 29, 'items': ['WarmogsArmor', 'ArchangelsStaff'], 'game_mode': 'Solo', 'traits': ['TFT14_StreetDemon_2', 'TFT14_Techie_3']},
        {'placement': 1, 'level': 8, 'gold_left': 2, 'damage': 141, 'items': ['InfinityEdge', 'GargoyleStoneplate'], 'game_mode': 'Solo', 'traits': ['TFT14_GodoftheNet_1', 'TFT14_BoomBots_4']},
        {'placement': 4, 'level': 9, 'gold_left': 0, 'damage': 80, 'items': ['InfinityEdge', 'Bloodthirster'], 'game_mode': 'Solo', 'traits': ['TFT14_Syndicate_3', 'TFT14_Vanguard_2']},
        {'placement': 7, 'level': 7, 'gold_left': 1, 'damage': 0, 'items': ['ArchangelsStaff', 'GuinsoosRageblade'], 'game_mode': 'Solo', 'traits': ['TFT14_Cypher_2', 'TFT14_Bastion_2']},
        {'placement': 2, 'level': 8, 'gold_left': 10, 'damage': 177, 'items': ['Morellonomicon', 'ThiefsGloves'], 'game_mode': 'Solo', 'traits': ['TFT14_Exotech_4', 'TFT14_Bastion_3']},
        {'placement': 6, 'level': 8, 'gold_left': 6, 'damage': 80, 'items': ['BlueBuff', 'WarmogsArmor'], 'game_mode': 'Solo', 'traits': ['TFT14_Exotech_2', 'TFT14_Bastion_2']},
        {'placement': 3, 'level': 9, 'gold_left': 0, 'damage': 112, 'items': ['DragonsClaw', 'GargoyleStoneplate'], 'game_mode': 'Solo', 'traits': ['TFT14_AnimaSquad_4', 'TFT14_Vanguard_3']},
        {'placement': 4, 'level': 8, 'gold_left': 1, 'damage': 32, 'items': ['ZekesHerald', 'InfinityEdge'], 'game_mode': 'Solo', 'traits': ['TFT14_GodoftheNet_1', 'TFT14_Cypher_3']},
        {'placement': 6, 'level': 8, 'gold_left': 0, 'damage': 95, 'items': ['BrambleVest', 'RunaansHurricane'], 'game_mode': 'Solo', 'traits': ['TFT14_AnimaSquad_3', 'TFT14_Exotech_2']},
        {'placement': 3, 'level': 9, 'gold_left': 1, 'damage': 152, 'items': ['WarmogsArmor', 'InfinityEdge'], 'game_mode': 'Solo', 'traits': ['TFT14_SoulKiller_1', 'TFT14_GoldenOx_2']},
        {'placement': 3, 'level': 8, 'gold_left': 0, 'damage': 137, 'items': ['WarmogsArmor', 'GargoyleStoneplate'], 'game_mode': 'Solo', 'traits': ['TFT14_GodoftheNet_1', 'TFT14_StreetDemon_3']},
        {'placement': 1, 'level': 9, 'gold_left': 7, 'damage': 201, 'items': ['ThiefsGloves', 'LastWhisper'], 'game_mode': 'Double Up', 'traits': ['TFT14_GodoftheNet_1', 'TFT14_StreetDemon_2']},
    ]
    
    return pd.DataFrame(matches_data)

def analyze_item_performance(df):
    """Analyze item performance and correlations"""
    item_stats = {}
    
    for _, match in df.iterrows():
        placement = match['placement']
        for item_name in match['items']:  # Items are already names, not IDs
            
            if item_name not in item_stats:
                item_stats[item_name] = {
                    'placements': [],
                    'games': 0,
                    'top4': 0
                }
            
            item_stats[item_name]['placements'].append(placement)
            item_stats[item_name]['games'] += 1
            if placement <= 4:
                item_stats[item_name]['top4'] += 1
    
    # Calculate averages and rates
    for item_name, stats in item_stats.items():
        if stats['games'] > 0:
            stats['avg_placement'] = np.mean(stats['placements'])
            stats['top4_rate'] = (stats['top4'] / stats['games']) * 100
        else:
            stats['avg_placement'] = 0
            stats['top4_rate'] = 0
    
    return pd.DataFrame.from_dict(item_stats, orient='index')

# Load data and generate insights
df = load_data()

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

# Handle case where item_performance might be empty
if not item_performance.empty and 'games' in item_performance.columns:
    item_performance_filtered = item_performance[item_performance['games'] >= min_item_games]
else:
    item_performance_filtered = pd.DataFrame()  # Empty DataFrame if no valid data

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

# Level vs Performance Analysis
st.markdown("---")
st.subheader("📊 Level vs Performance Analysis")

# Calculate average placement by level
if len(df_filtered) > 0:
    level_summary = df_filtered.groupby('level').agg({
        'placement': 'mean'
    }).round(2)
    level_summary['games'] = df_filtered.groupby('level').size()
    level_summary = level_summary.reset_index()

    # Invert the placement values so better performance = taller bars
    level_summary['inverted_placement'] = 9 - level_summary['placement']

    # Create bar chart with inverted values
    fig_level = px.bar(
        level_summary, 
        x='level', 
        y='inverted_placement',
        title="Performance by Final Level Reached",
        color='placement',
        color_continuous_scale='RdYlGn_r',
        text='games'
    )

    # Update layout for better readability
    fig_level.update_layout(
        yaxis=dict(
            title="Performance Score (Taller = Better)",
            range=[0, 8]
        ),
        xaxis=dict(title="Final Level Reached"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    # Add game count labels on bars
    fig_level.update_traces(
        texttemplate='%{text} games', 
        textposition='outside',
        textfont_size=12
    )

    st.plotly_chart(fig_level, use_container_width=True)
else:
    st.info("No data available for level analysis")

# Charts Grid
st.markdown("---")
st.subheader("📊 Performance Analysis")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Item performance chart - VERTICAL BARS WITH ICONS
    if not item_performance_filtered.empty and len(item_performance_filtered) > 0:
        best_items = item_performance_filtered.nsmallest(8, 'avg_placement')
        
        if len(best_items) > 0:
            # Create inverted performance score (same as level analysis)
            best_items_data = best_items.reset_index()
            best_items_data['performance_score'] = 9 - best_items_data['avg_placement']
            best_items_data['clean_names'] = best_items_data['index'].apply(clean_item_name)
            
            fig_item_perf = px.bar(
                best_items_data,
                x='clean_names',
                y='performance_score',
                title="🏆 Best Items by Performance",
                color='avg_placement',
                color_continuous_scale='RdYlGn_r',
                text='games'
            )
            
            # Add item icons as images on x-axis
            icon_urls = [get_item_icon_url(clean_item_name(item)) for item in best_items_data['index']]
            
            fig_item_perf.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(title="Performance Score (Taller = Better)"),
                xaxis=dict(
                    title="Item",
                    tickmode='array',
                    tickvals=list(range(len(best_items_data))),
                    ticktext=[''] * len(best_items_data),  # Remove text labels
                ),
                showlegend=False,
                images=[
                    dict(
                        source=url,
                        xref="x", yref="paper",
                        x=i, y=-0.15,
                        sizex=0.8, sizey=0.1,
                        xanchor="center", yanchor="middle"
                    ) for i, url in enumerate(icon_urls)
                ]
            )
            
            fig_item_perf.update_traces(
                texttemplate='%{text} games', 
                textposition='outside',
                textfont_size=10
            )
            st.plotly_chart(fig_item_perf, use_container_width=True)
        else:
            st.info(f"Not enough item data for {selected_mode} games with minimum {min_item_games} usage")
    else:
        st.info(f"Not enough item data for {selected_mode} games with minimum {min_item_games} usage")

with chart_col2:
    # Trait vs Placement Analysis (FIXED VERSION)
    st.markdown("### 🎭 Trait Performance")
    
    if len(df_filtered) > 0 and 'traits' in df_filtered.columns:
        # Debug information
        with st.expander("🔍 Debug Trait Data", expanded=False):
            st.markdown(f"* Total games: {len(df_filtered)}")
            st.markdown(f"* Columns available: {list(df_filtered.columns)}")
            st.markdown(f"* 'traits' column exists {'✅' if 'traits' in df_filtered.columns else '❌'}")
            
            # Show first few games' trait data
            st.markdown("**First 5 games trait data:**")
            for idx, (_, row) in enumerate(df_filtered.head(5).iterrows()):
                trait_data = row['traits'] if 'traits' in row else []
                st.markdown(f"Game {idx+1}: {trait_data} (type: {type(trait_data)})")
            
            # Count games with non-empty traits
            non_empty_traits = df_filtered[df_filtered['traits'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False)]
            st.markdown(f"* Games with non-empty traits: {len(non_empty_traits)}/{len(df_filtered)}")
            
            # Show some examples
            if len(non_empty_traits) > 0:
                examples = non_empty_traits['traits'].head(3).tolist()
                st.markdown(f"* Trait examples: {examples}")
        
        # Extract trait-placement pairs with improved parsing
        trait_placements = []
        
        for idx, (_, match) in enumerate(df_filtered.iterrows()):
            if match['traits'] and len(match['traits']) > 0:
                placement = match['placement']
                
                for trait_entry in match['traits']:
                    if isinstance(trait_entry, str) and trait_entry != 'TFT14':
                        # Handle different possible formats:
                        # Format 1: 'TFT14_Armorclad_2'
                        # Format 2: 'Armorclad_2' 
                        # Format 3: Just 'Armorclad'
                        
                        if '_' in trait_entry:
                            parts = trait_entry.split('_')
                            
                            if len(parts) >= 3 and parts[0] == 'TFT14':
                                # Format: TFT14_Armorclad_2
                                trait_name = parts[1]
                                trait_tier = parts[2] if parts[2].isdigit() else '1'
                            elif len(parts) >= 2:
                                # Format: Armorclad_2 or similar
                                trait_name = parts[0]
                                trait_tier = parts[1] if parts[1].isdigit() else '1'
                            else:
                                # Format: Just trait name
                                trait_name = trait_entry
                                trait_tier = '1'
                        else:
                            # No underscores, just trait name
                            trait_name = trait_entry
                            trait_tier = '1'
                        
                        # Only add if we got a valid trait name that's not just 'TFT14'
                        if trait_name and trait_name != 'TFT14' and len(trait_name) > 2:
                            trait_placements.append({
                                'trait': trait_name,
                                'trait_with_tier': f"{trait_name} ({trait_tier})",
                                'placement': placement,
                                'tier': trait_tier
                            })
        
        if trait_placements:
            trait_df = pd.DataFrame(trait_placements)
            
            # Calculate average placement by trait (only show traits with 2+ games)
            trait_summary = trait_df.groupby('trait').agg({
                'placement': ['mean', 'count']
            }).round(2)
            trait_summary.columns = ['avg_placement', 'games']
            trait_summary = trait_summary[trait_summary['games'] >= 2]  # Lowered threshold
            
            if len(trait_summary) > 0:
                trait_summary = trait_summary.reset_index()
                trait_summary['performance_score'] = 9 - trait_summary['avg_placement']
                
                # Create vertical bar chart
                fig_trait = px.bar(
                    trait_summary.nlargest(8, 'performance_score'),  # Show top 8
                    x='trait',
                    y='performance_score',
                    title="Best Traits by Performance",
                    color='avg_placement',
                    color_continuous_scale='RdYlGn_r',
                    text='games'
                )
                fig_trait.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis=dict(title="Performance Score (Higher = Better)"),
                    xaxis=dict(title="Main Trait", tickangle=45),
                    showlegend=False,
                    height=400
                )
                fig_trait.update_traces(
                    texttemplate='%{text} games', 
                    textposition='outside',
                    textfont_size=10
                )
                st.plotly_chart(fig_trait, use_container_width=True)
                
                # Show trait summary table
                st.markdown("**Trait Performance Summary:**")
                display_trait_df = trait_summary[['trait', 'avg_placement', 'games']].copy()
                display_trait_df['avg_placement'] = display_trait_df['avg_placement'].round(2)
                st.dataframe(display_trait_df, use_container_width=True, hide_index=True)
                
            else:
                st.info("Need more games with each trait (2+ games) for analysis")
        else:
            st.error("❌ No valid trait data found! The API data extraction needs to be fixed.")
            st.markdown("**Possible issues:**")
            st.markdown("- API script isn't extracting trait names properly")
            st.markdown("- Trait data is coming through as just 'TFT14' without actual trait names")
            st.markdown("- Need to check the trait extraction in `clean_tft_analyzer.py`")
    else:
        st.info("No trait data available for analysis")

# Game Mode Comparison (NEW)
if selected_mode == 'All' and len(df['game_mode'].unique()) > 1:
    st.markdown("---")
    st.subheader("⚔️ Solo vs Double Up Performance")
    
    mode_comparison = df.groupby('game_mode').agg({
        'placement': 'mean',
        'level': 'mean',
        'damage': 'mean',
        'game_mode': 'count'
    }).round(2)
    mode_comparison.columns = ['avg_placement', 'avg_level', 'avg_damage', 'games']
    
    col1, col2, col3 = st.columns(3)
    
    for i, (mode, stats) in enumerate(mode_comparison.iterrows()):
        with [col1, col2, col3][i % 3]:
            st.metric(
                f"{mode} ({stats['games']} games)", 
                f"{stats['avg_placement']:.2f} avg placement",
                delta=f"{4.5 - stats['avg_placement']:+.2f}"
            )
            st.caption(f"Level {stats['avg_level']:.1f} • {stats['avg_damage']:.0f} damage")

# Key Takeaways Section - Dynamic based on actual data
st.markdown("---")
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

# Detailed Item Analysis
st.markdown("---")
st.subheader("⚔️ Detailed Item Statistics")

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
                # Convert stats to dictionary format
                stats_dict = {
                    'games': int(stats['games']),
                    'avg_placement': float(stats['avg_placement']), 
                    'top4_rate': float(stats['top4_rate']),
                    'placements': stats.get('placements', [])
                }
                display_item_with_icon(item, stats_dict)
                st.markdown("---")
        else:
            st.info("No items meet the criteria for best performers")

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
                # Convert stats to dictionary format
                stats_dict = {
                    'games': int(stats['games']),
                    'avg_placement': float(stats['avg_placement']), 
                    'top4_rate': float(stats['top4_rate']),
                    'placements': stats.get('placements', [])
                }
                display_item_with_icon(item, stats_dict)
                st.markdown("---")
        else:
            st.info("No items meet the criteria for problem items")

with tab3:
    st.markdown("### 📈 Most Used Items")
    st.markdown("Items you use most frequently, regardless of performance:")
    
    if not item_performance_filtered.empty:
        most_used_items = item_performance_filtered.nlargest(10, 'games')
        
        for item, stats in most_used_items.iterrows():
            # Convert stats to dictionary format - EXACTLY like other tabs
            stats_dict = {
                'games': int(stats['games']),
                'avg_placement': float(stats['avg_placement']), 
                'top4_rate': float(stats['top4_rate']),
                'placements': stats.get('placements', [])
            }
            
            # Use the same display function as other tabs
            display_item_with_icon(item, stats_dict)
            st.markdown("---")
    else:
        st.info("No item data available for the selected criteria.")

# Recent Games History
st.markdown("---")
st.subheader("📋 Recent Games History")

# Show last 10 games in a nice format
recent_games = df_filtered.head(10).copy()
recent_games['placement_emoji'] = recent_games['placement'].apply(
    lambda x: "🥇" if x == 1 else "🥈" if x == 2 else "🥉" if x == 3 else "✅" if x <= 4 else "❌"
)

# Create columns for the recent games display
for idx, (_, game) in enumerate(recent_games.iterrows()):
    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 3])
    
    with col1:
        st.markdown(f"**Game {idx+1}**")
        st.markdown(f"{game['placement_emoji']} #{game['placement']}")
    
    with col2:
        st.markdown(f"**Level {game['level']}**")
        st.caption(f"{game['damage']} damage")
    
    with col3:
        st.markdown(f"**Gold: {game['gold_left']}**")
        st.caption(f"{len(game['items'])} items")
    
    with col4:
        # Show top 2 items
        top_items = game['items'][:2] if len(game['items']) >= 2 else game['items']
        st.markdown("**Items:**")
        for item in top_items:
            st.caption(f"• {clean_item_name(item)}")
    
    with col5:
        # Show top 2 traits
        if game['traits'] and len(game['traits']) > 0:
            st.markdown("**Traits:**")
            traits_to_show = game['traits'][:2]
            for trait in traits_to_show:
                if isinstance(trait, str) and '_' in trait:
                    parts = trait.split('_')
                    if len(parts) >= 2:
                        trait_name = parts[1] if parts[0] == 'TFT14' else parts[0]
                        trait_tier = parts[2] if len(parts) >= 3 else parts[1]
                        st.caption(f"• {trait_name} ({trait_tier})")
                else:
                    st.caption(f"• {trait}")
    
    if idx < len(recent_games) - 1:
        st.markdown("---")

# Performance Trends
st.markdown("---")
st.subheader("📈 Performance Trends")

if len(df_filtered) >= 10:
    # Create a rolling average of placement
    df_trends = df_filtered.head(20).copy()
    df_trends['game_number'] = range(1, len(df_trends) + 1)
    df_trends['rolling_avg'] = df_trends['placement'].rolling(window=5, min_periods=1).mean()
    
    fig_trend = px.line(
        df_trends,
        x='game_number',
        y='rolling_avg',
        title="Placement Trend (5-game rolling average)",
        markers=True
    )
    
    # Add reference line at 4.5 (average placement)
    fig_trend.add_hline(y=4.5, line_dash="dash", line_color="gray", 
                       annotation_text="Average (4.5)")
    
    fig_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title="Average Placement (Lower = Better)", autorange="reversed"),
        xaxis=dict(title="Game Number (Most Recent → Oldest)")
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("Need at least 10 games for trend analysis")

# Footer
st.markdown("---")
st.markdown("*Dashboard updates automatically when you run new analysis. Data refreshes with each game session.*")
