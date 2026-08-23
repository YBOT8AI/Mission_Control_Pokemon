// YBOT Unified Backend - All Projects in One API
// OrbitX NFT + KINKIN

const { createClient } = require('@supabase/supabase-js');

export default async function handler(request, response) {
  // Enable CORS
  response.setHeader('Access-Control-Allow-Origin', '*');
  response.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  response.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (request.method === 'OPTIONS') {
    return response.status(200).end();
  }
  
  try {
    // Initialize Supabase client
    const supabase = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_SERVICE_ROLE_KEY
    );
    
    const { method, query, body } = request;
    
    // Route: /api?project=orbitx&table=artists
    const project = query.project || body?.project;
    const table = query.table || body?.table;
    
    if (!project) {
      return response.status(200).json({
        name: 'YBOT Unified Backend',
        version: '1.0.0',
        projects: ['orbitx', 'kinkin'],
        usage: 'GET /api?project=orbitx&table=artists',
        stats: 'GET /api?project=orbitx&stats=true'
      });
    }
    
    // ==================== ORBITX NFT ====================
    if (project === 'orbitx') {
      
      if (method === 'GET') {
        // Get stats
        if (query.stats === 'true') {
          const { count: artistsCount } = await supabase.from('orbitx_artists').select('*', { count: 'exact', head: true });
          const { count: artworksCount } = await supabase.from('orbitx_artworks').select('*', { count: 'exact', head: true });
          
          return response.status(200).json({
            success: true,
            data: {
              totalArtists: artistsCount || 0,
              totalArtworks: artworksCount || 0,
              phase: '1 - Fine Arts',
              lastUpdated: new Date().toISOString()
            }
          });
        }
        
        // Get table data
        if (table) {
          const tableName = `orbitx_${table}`;
          let q = supabase.from(tableName).select('*');
          
          // Apply filters
          if (query.artist_id) q = q.eq('artist_id', query.artist_id);
          if (query.status) q = q.eq('status', query.status);
          if (query.approved === 'true') q = q.eq('approved', true);
          
          const { data, error } = await q.order('created_at', { ascending: false }).limit(100);
          
          if (error) throw error;
          return response.status(200).json({ success: true, data, project: 'orbitx', table });
        }
      }
      
      // POST - Create record
      if (method === 'POST') {
        const { id, ...recordData } = body;
        const tableName = `orbitx_${table}`;
        
        const { data, error } = await supabase.from(tableName).insert([recordData]).select();
        
        if (error) throw error;
        return response.status(201).json({ success: true, data, project: 'orbitx' });
      }
      
      // PUT - Update record
      if (method === 'PUT') {
        const { id, ...updateData } = body;
        const tableName = `orbitx_${table}`;
        
        const { data, error } = await supabase.from(tableName).update(updateData).eq('id', id).select();
        
        if (error) throw error;
        return response.status(200).json({ success: true, data, project: 'orbitx' });
      }
    }
    
    // ==================== KINKIN ====================
    if (project === 'kinkin') {
      
      if (method === 'GET') {
        // Get stats
        if (query.stats === 'true') {
          const { count: providersCount } = await supabase.from('kinkin_providers').select('*', { count: 'exact', head: true });
          const { count: bookingsCount } = await supabase.from('kinkin_bookings').select('*', { count: 'exact', head: true });
          
          return response.status(200).json({
            success: true,
            data: {
              totalProviders: providersCount || 0,
              totalBookings: bookingsCount || 0,
              lastUpdated: new Date().toISOString()
            }
          });
        }
        
        // Get table data
        if (table) {
          const tableName = `kinkin_${table}`;
          let q = supabase.from(tableName).select('*');
          
          if (query.provider_id) q = q.eq('provider_id', query.provider_id);
          if (query.category) q = q.eq('category', query.category);
          if (query.status) q = q.eq('status', query.status);
          if (query.verified === 'true') q = q.eq('verified', true);
          
          const { data, error } = await q.order('created_at', { ascending: false }).limit(100);
          
          if (error) throw error;
          return response.status(200).json({ success: true, data, project: 'kinkin', table });
        }
      }
      
      // POST - Create record
      if (method === 'POST') {
        const { id, ...recordData } = body;
        const tableName = `kinkin_${table}`;
        
        const { data, error } = await supabase.from(tableName).insert([recordData]).select();
        
        if (error) throw error;
        return response.status(201).json({ success: true, data, project: 'kinkin' });
      }
      
      // PUT - Update record
      if (method === 'PUT') {
        const { id, ...updateData } = body;
        const tableName = `kinkin_${table}`;
        
        const { data, error } = await supabase.from(tableName).update(updateData).eq('id', id).select();
        
        if (error) throw error;
        return response.status(200).json({ success: true, data, project: 'kinkin' });
      }
    }
    
    return response.status(400).json({ 
      success: false, 
      error: 'Invalid project. Use: orbitx or kinkin' 
    });
    
  } catch (error) {
    console.error('YBOT API Error:', error);
    return response.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
}
