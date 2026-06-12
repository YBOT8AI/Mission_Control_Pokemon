// Lightweight Vercel Serverless Function - No auth required
// Fetches public GitHub data and workspace status

export default async function handler(request, response) {
  // Enable CORS
  response.setHeader('Access-Control-Allow-Origin', '*');
  response.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  response.setHeader('Cache-Control', 'max-age=0, s-maxage=60, stale-while-revalidate=300');
  
  if (request.method === 'OPTIONS') {
    return response.status(200).end();
  }
  
  try {
    // Fetch public GitHub repo data (no auth needed for public repos)
    const repos = [
      { key: 'orbitx', name: 'Orbitx-NFT' },
      { key: 'kinkin', name: 'KINKIN' },
      { key: 'clientTracker', name: 'Client_Tracker_Pro' },
      { key: 'dashboard', name: 'Dashboard' }
    ];
    
    const repoStatus = {};
    
    for (const repo of repos) {
      try {
        const ghRes = await fetch(`https://api.github.com/repos/YBOT8AI/${repo.name}`, {
          headers: { 'User-Agent': 'YBOT-Mission-Control' }
        });
        
        if (ghRes.ok) {
          const data = await ghRes.json();
          
          // Get latest commit
          const commitRes = await fetch(`https://api.github.com/repos/YBOT8AI/${repo.name}/commits?per_page=1`, {
            headers: { 'User-Agent': 'YBOT-Mission-Control' }
          });
          
          let lastCommit = null;
          if (commitRes.ok) {
            const commits = await commitRes.json();
            if (commits.length > 0) {
              lastCommit = {
                sha: commits[0].sha.substring(0, 7),
                message: commits[0].commit.message.split('\n')[0],
                time: commits[0].commit.author.date,
                author: commits[0].commit.author.name
              };
            }
          }
          
          repoStatus[repo.key] = {
            stars: data.stargazers_count,
            forks: data.forks_count,
            updatedAt: data.updated_at,
            lastCommit,
            openIssues: data.open_issues_count,
            size: data.size,
            language: data.language
          };
        }
      } catch (err) {
        console.error(`Failed to fetch ${repo.name}:`, err.message);
      }
    }
    
    // Build dashboard data
    const now = new Date().toISOString();
    
    const dashboardData = {
      lastUpdated: now,
      source: 'live-github-api',
      refreshInterval: 60, // seconds
      
      projects: {
        orbitx: {
          name: 'OrbitX NFT',
          emoji: '🌌',
          pokemon: 'Mewtwo',
          pokemonId: 150,
          status: repoStatus.orbitx?.lastCommit ? 'active' : 'standby',
          phase: '1 - Fine Arts',
          progress: calculateProgress(repoStatus.orbitx),
          testnet: 'pending',
          repo: 'YBOT8AI/Orbitx-NFT',
          github: repoStatus.orbitx,
          tasks: [
            { name: 'Frontend Development', completed: true },
            { name: 'Smart Contract Setup', completed: true },
            { name: 'WalletConnect Integration', completed: true },
            { name: 'Testnet Deployment', completed: false },
            { name: 'Artist Outreach', completed: false }
          ]
        },
        
        kinkin: {
          name: 'KINKIN',
          emoji: '🚀',
          pokemon: 'Pikachu',
          pokemonId: 25,
          status: repoStatus.kinkin?.lastCommit ? 'active' : 'deploying',
          progress: calculateProgress(repoStatus.kinkin),
          url: 'kinkin.vercel.app',
          build: 5,
          repo: 'YBOT8AI/KINKIN',
          github: repoStatus.kinkin,
          tasks: [
            { name: 'Core Marketplace', completed: true },
            { name: 'Provider Profiles', completed: true },
            { name: 'Booking Flow', completed: false },
            { name: 'Payment Integration', completed: false },
            { name: 'Mobile App', completed: false }
          ]
        },
        
        techwealth: {
          name: 'TechWealth',
          emoji: '💼',
          pokemon: 'Meowth',
          pokemonId: 52,
          status: 'planning',
          focus: 'Financial Tech',
          stage: 'concept',
          progress: 25,
          tasks: [
            { name: 'Concept Definition', completed: true },
            { name: 'Market Research', completed: false },
            { name: 'MVP Planning', completed: false },
            { name: 'Development', completed: false }
          ]
        },
        
        wpo: {
          name: 'WPO (World Paws Org)',
          emoji: '🐾',
          pokemon: 'Chansey',
          pokemonId: 113,
          status: 'building',
          phase: 'Option B - Full Build',
          blockchain: 'Solana',
          token: 'WPO Token (SPL)',
          progress: 45,
          logo: 'received',
          youtube: 'planned',
          tasks: [
            { name: 'Mission Definition', completed: true },
            { name: 'Option B Selected', completed: true },
            { name: 'Logo Received', completed: true },
            { name: 'Solana Token Setup', completed: false },
            { name: 'Website Development', completed: false },
            { name: 'GitHub Repository', completed: false },
            { name: 'Vercel Deployment', completed: false },
            { name: 'YouTube Channel Setup', completed: false }
          ]
        },
        
        clientTracker: {
          name: 'Client Tracker Pro',
          emoji: '📊',
          pokemon: 'Kadabra',
          pokemonId: 64,
          status: repoStatus.clientTracker?.lastCommit ? 'active' : 'building',
          progress: calculateProgress(repoStatus.clientTracker),
          repo: 'YBOT8AI/Client_Tracker_Pro',
          github: repoStatus.clientTracker,
          tasks: [
            { name: 'Dashboard UI', completed: true },
            { name: 'Client Forms', completed: true },
            { name: 'Purchase Tracking', completed: true },
            { name: 'Referral System', completed: true },
            { name: 'GitHub Upload', completed: true },
            { name: 'Vercel Deploy', completed: false },
            { name: 'Supabase Setup', completed: false }
          ]
        },
        
        dashboard: {
          name: 'Mission Control Dashboard',
          emoji: '🎯',
          pokemon: 'Articuno',
          pokemonId: 144,
          status: repoStatus.dashboard?.lastCommit ? 'active' : 'online',
          progress: 100,
          repo: 'YBOT8AI/Dashboard',
          github: repoStatus.dashboard,
          url: 'ybot-mission-control-delta.vercel.app',
          tasks: [
            { name: 'Multi-page Navigation', completed: true },
            { name: 'Live API Integration', completed: true },
            { name: 'Auto-refresh', completed: true },
            { name: 'GitHub Sync', completed: true }
          ]
        }
      },
      
      agents: {
        ybot: { name: 'YBOT (Main)', status: 'online', emoji: '⚡', role: 'Overall Coordination' },
        agentx: { 
          name: 'Agent X 🌌', 
          status: 'active', 
          role: 'OrbitX NFT Operations',
          respawn: 'Every 5 min',
          workspace: '/root/.openclaw/workspace-orbitx/'
        },
        agentkinkin: { 
          name: 'Agent KinKin 🚀', 
          status: 'active', 
          role: 'KINKIN Marketplace',
          respawn: 'Every 5 min',
          workspace: '/root/.openclaw/workspace-kinkin/'
        },
        bulle: { 
          name: 'Bull-E 🐂', 
          status: 'standby', 
          role: 'Market Intelligence',
          lastBriefing: '2026-06-10T19:58:31Z',
          schedule: '01:00/07:00/13:00 UTC (09:00/15:00/21:00 HKT)',
          workspace: '/root/.openclaw/workspace-bull-e/'
        },
        heartbeat: { name: 'Heartbeat Scan', status: 'active', interval: '30 min' },
        ceobriefing: { name: 'CEO Briefing', status: 'scheduled', frequency: '3x daily (HKT)' },
        gateway: { name: 'Gateway', status: 'running', host: 'srv1595219' }
      },
      
      activity: generateActivityLog(repoStatus, now),
      
      goals: [
        { name: 'OrbitX Phase 2', desc: 'Music NFT marketplace expansion', priority: 'high' },
        { name: 'KINKIN Mobile App', desc: 'iOS + Android launch', priority: 'high' },
        { name: 'TechWealth Launch', desc: 'Financial tech platform MVP', priority: 'medium' },
        { name: 'WPO Token', desc: 'World Paws Organization token launch', priority: 'medium' }
      ],
      
      systemHealth: {
        github: 'connected',
        vercel: 'auto-deploy enabled',
        lastSync: now
      }
    };
    
    return response.status(200).json(dashboardData);
    
  } catch (error) {
    console.error('API Error:', error);
    return response.status(500).json({ 
      error: 'Failed to fetch dashboard data',
      message: error.message,
      fallback: true
    });
  }
}

// Helper: Calculate progress based on GitHub activity
function calculateProgress(githubData) {
  if (!githubData) return 50;
  
  let progress = 60; // Base progress for active repos
  
  // Recent commits = active development
  if (githubData.lastCommit) {
    const lastCommitDate = new Date(githubData.lastCommit.time);
    const daysSinceCommit = (Date.now() - lastCommitDate.getTime()) / (1000 * 60 * 60 * 24);
    
    if (daysSinceCommit < 1) progress = 90;  // Today
    else if (daysSinceCommit < 2) progress = 85;  // Yesterday
    else if (daysSinceCommit < 3) progress = 80;  // This week
    else if (daysSinceCommit < 7) progress = 70;  // This month
    else progress = 60;  // Older
  }
  
  // More stars/forks = more mature
  if (githubData.stars > 10) progress = Math.min(progress + 5, 95);
  if (githubData.forks > 5) progress = Math.min(progress + 3, 95);
  
  return progress;
}

// Helper: Generate activity log from real data
function generateActivityLog(repoStatus, now) {
  const activities = [];
  
  // Add recent GitHub activity
  Object.entries(repoStatus).forEach(([key, data]) => {
    if (data?.lastCommit) {
      activities.push({
        time: data.lastCommit.time,
        type: 'success',
        text: `${key.toUpperCase()}: ${data.lastCommit.message} (${data.lastCommit.sha})`
      });
    }
  });
  
  // Sort by time (newest first)
  activities.sort((a, b) => new Date(b.time) - new Date(a.time));
  
  // Add system message
  activities.unshift({
    time: now,
    type: 'info',
    text: '📊 Dashboard refreshed from live GitHub API'
  });
  
  return activities.slice(0, 20);
}
