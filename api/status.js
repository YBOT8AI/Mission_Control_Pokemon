// Vercel Serverless Function - Dynamic Dashboard Data
// Fetches real-time data from GitHub, Vercel, and workspace

export default async function handler(request, response) {
  // Enable CORS
  response.setHeader('Access-Control-Allow-Origin', '*');
  response.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  response.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (request.method === 'OPTIONS') {
    return response.status(200).end();
  }
  
  try {
    const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
    const VERCEL_TOKEN = process.env.VERCEL_TOKEN;
    const PROJECT_ID = 'prj_iLm0JgO3lAdHpMpSzAp8rVGB8ccX';
    
    // Fetch GitHub repo status for all projects
    const repos = [
      { key: 'orbitx', name: 'Orbitx-NFT' },
      { key: 'kinkin', name: 'KINKIN' },
      { key: 'clientTracker', name: 'Client_Tracker_Pro' }
    ];
    
    const repoStatus = {};
    
    // Fetch each repo's latest commit and activity
    for (const repo of repos) {
      try {
        const ghRes = await fetch(`https://api.github.com/repos/YBOT8AI/${repo.name}`, {
          headers: GITHUB_TOKEN ? { Authorization: `token ${GITHUB_TOKEN}` } : {}
        });
        
        if (ghRes.ok) {
          const data = await ghRes.json();
          
          // Get latest commit
          const commitRes = await fetch(`https://api.github.com/repos/YBOT8AI/${repo.name}/commits`, {
            headers: GITHUB_TOKEN ? { Authorization: `token ${GITHUB_TOKEN}` } : {}
          });
          
          let lastCommit = null;
          if (commitRes.ok) {
            const commits = await commitRes.json();
            if (commits.length > 0) {
              lastCommit = {
                sha: commits[0].sha.substring(0, 7),
                message: commits[0].commit.message.split('\n')[0],
                time: commits[0].commit.author.date
              };
            }
          }
          
          repoStatus[repo.key] = {
            stars: data.stargazers_count,
            forks: data.forks_count,
            updatedAt: data.updated_at,
            lastCommit,
            openIssues: data.open_issues_count
          };
        }
      } catch (err) {
        console.error(`Failed to fetch ${repo.name}:`, err);
      }
    }
    
    // Fetch Vercel deployment status
    let deploymentStatus = null;
    try {
      const vercelRes = await fetch(`https://api.vercel.com/v13/deployments?projectId=${PROJECT_ID}`, {
        headers: VERCEL_TOKEN ? { Authorization: `Bearer ${VERCEL_TOKEN}` } : {}
      });
      
      if (vercelRes.ok) {
        const deployments = await vercelRes.json();
        if (deployments.deployments && deployments.deployments.length > 0) {
          const latest = deployments.deployments[0];
          deploymentStatus = {
            state: latest.state, // READY, BUILDING, ERROR, etc.
            url: latest.url,
            createdAt: latest.createdAt,
            buildNumber: deployments.deployments.length
          };
        }
      }
    } catch (err) {
      console.error('Failed to fetch Vercel status:', err);
    }
    
    // Build dynamic dashboard data
    const dashboardData = {
      lastUpdated: new Date().toISOString(),
      source: 'live-api',
      
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
          status: deploymentStatus?.state === 'READY' ? 'online' : (deploymentStatus?.state === 'BUILDING' ? 'building' : 'deploying'),
          progress: deploymentStatus ? 80 : 60,
          url: deploymentStatus?.url || 'kinkin.vercel.app',
          build: deploymentStatus?.buildNumber || 5,
          repo: 'YBOT8AI/KINKIN',
          github: repoStatus.kinkin,
          vercel: deploymentStatus,
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
          status: 'planning',
          progress: 33,
          tasks: [
            { name: 'Mission Definition', completed: true },
            { name: 'Token Economics', completed: false },
            { name: 'Partnership Outreach', completed: false }
          ]
        },
        
        clientTracker: {
          name: 'Client Tracker Pro',
          emoji: '📊',
          pokemon: 'Kadabra',
          pokemonId: 64,
          status: repoStatus.clientTracker?.lastCommit ? 'active' : 'building',
          progress: repoStatus.clientTracker ? 85 : 60,
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
        }
      },
      
      agents: {
        ybot: { name: 'YBOT (Main)', status: 'online', emoji: '⚡' },
        heartbeat: { name: 'Heartbeat Scan', status: 'active', interval: '30 min' },
        ceobriefing: { name: 'CEO Briefing', status: 'scheduled', frequency: '3x daily' },
        gateway: { name: 'Gateway', status: 'running', host: 'srv1595219' }
      },
      
      activity: generateActivityLog(repoStatus, deploymentStatus),
      
      goals: [
        { name: 'OrbitX Phase 2', desc: 'Music NFT marketplace expansion', priority: 'high' },
        { name: 'KINKIN Mobile App', desc: 'iOS + Android launch', priority: 'high' },
        { name: 'TechWealth Launch', desc: 'Financial tech platform MVP', priority: 'medium' },
        { name: 'WPO Token', desc: 'World Paws Organization token launch', priority: 'medium' }
      ]
    };
    
    return response.status(200).json(dashboardData);
    
  } catch (error) {
    console.error('API Error:', error);
    return response.status(500).json({ 
      error: 'Failed to fetch dashboard data',
      message: error.message 
    });
  }
}

// Helper: Calculate progress based on GitHub activity
function calculateProgress(githubData) {
  if (!githubData) return 50;
  
  let progress = 50; // Base progress
  
  // Recent commits = active development
  if (githubData.lastCommit) {
    const lastCommitDate = new Date(githubData.lastCommit.time);
    const daysSinceCommit = (Date.now() - lastCommitDate.getTime()) / (1000 * 60 * 60 * 24);
    
    if (daysSinceCommit < 1) progress += 20;  // Today
    else if (daysSinceCommit < 3) progress += 15;  // This week
    else if (daysSinceCommit < 7) progress += 10;  // This month
  }
  
  // More stars/forks = more mature
  if (githubData.stars > 10) progress += 5;
  if (githubData.forks > 5) progress += 5;
  
  return Math.min(progress, 95); // Cap at 95%
}

// Helper: Generate activity log from real data
function generateActivityLog(repoStatus, deploymentStatus) {
  const activities = [];
  const now = new Date();
  
  // Add recent GitHub activity
  Object.entries(repoStatus).forEach(([key, data]) => {
    if (data?.lastCommit) {
      activities.push({
        time: data.lastCommit.time,
        type: 'success',
        text: `${key.toUpperCase()}: ${data.lastCommit.message}`
      });
    }
  });
  
  // Add Vercel deployment
  if (deploymentStatus) {
    activities.push({
      time: deploymentStatus.createdAt,
      type: deploymentStatus.state === 'READY' ? 'success' : 'info',
      text: `Vercel deployment: ${deploymentStatus.state}`
    });
  }
  
  // Sort by time (newest first)
  activities.sort((a, b) => new Date(b.time) - new Date(a.time));
  
  // Add system messages
  activities.push({
    time: now.toISOString(),
    type: 'info',
    text: 'Dashboard data refreshed from live API'
  });
  
  return activities.slice(0, 20); // Keep last 20
}
