import axios from "axios";
import jwt from 'jsonwebtoken';
import dotenv from "dotenv";

dotenv.config(); // Load environment variables from .env file

const FEEDMOB_API_BASE = process.env.FEEDMOB_API_BASE;
const FEEDMOB_KEY = process.env.FEEDMOB_KEY;
const FEEDMOB_SECRET = process.env.FEEDMOB_SECRET;

if (!FEEDMOB_KEY || !FEEDMOB_SECRET) {
  console.error("Error: FEEDMOB_KEY and FEEDMOB_SECRET environment variables must be set.");
  process.exit(1);
}

// Generate JWT token
function generateToken(key: string, secret: string): string {
  const expirationDate = new Date();
  expirationDate.setDate(expirationDate.getDate() + 7); // 7 days from now

  const payload = {
    key: key,
    expired_at: expirationDate.toISOString().split('T')[0] // Format as YYYY-MM-DD
  };

  return jwt.sign(payload, secret, { algorithm: 'HS256' });
}

// Helper Function for API Call
export async function fetchDirectSpendsData(
  client_id: number,
  start_date: string,
  end_date: string,
  vendor_id?: number,
  click_url_ids?: string
): Promise<any> {
  const url = `${FEEDMOB_API_BASE}/ai/api/direct_spends?client_id=${client_id}&start_date=${start_date}&end_date=${end_date}${vendor_id ? `&vendor_id=${vendor_id}` : ''}${click_url_ids ? `&click_url_id=${click_url_ids}` : ''}`;

  try {
    const token = generateToken(FEEDMOB_KEY as string, FEEDMOB_SECRET as string);
    const response = await axios.get(url, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'FEEDMOB-KEY': FEEDMOB_KEY,
        'FEEDMOB-TOKEN': token
      },
      timeout: 30000,
    });
    return response.data;
  } catch (error: unknown) {
    console.error("Error fetching direct spends data from FeedMob API:", error);
    if (error && typeof error === 'object' && 'response' in error) {
      const err = error as Record<string, any>;
      const status = err.response?.status;
      if (status === 401) {
        throw new Error('FeedMob API request failed: Unauthorized (Invalid API Key or Token)');
      } else if (status === 400) {
        throw new Error('FeedMob API request failed: Bad Request');
      } else if (status === 404) {
        throw new Error('FeedMob API request failed: Not Found');
      } else {
        throw new Error(`FeedMob API request failed: ${status || 'Unknown error'}`);
      }
    }
    throw new Error('Failed to fetch direct spends data from FeedMob API');
  }
}

export async function fetchInmobiCampaignMappingsData(): Promise<any> {
  const url = `${FEEDMOB_API_BASE}/ai/api/inmobi_campaign_mappings`;
  try {
    // Generate a fresh token for each request
    const token = generateToken(FEEDMOB_KEY as string, FEEDMOB_SECRET as string);

    const response = await axios.get(url, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'FEEDMOB-KEY': FEEDMOB_KEY,
        'FEEDMOB-TOKEN': token
      },
      timeout: 30000, // 30 second timeout
    });
    return response.data;
  } catch (error: unknown) {
    console.error("Error fetching data from FeedMob API:", error);
    if (error && typeof error === 'object' && 'response' in error) {
      const err = error as Record<string, any>;
      const status = err.response?.status;
      if (status === 401) {
        throw new Error('FeedMob API request failed: Unauthorized (Invalid API Key or Token)');
      } else if (status === 400) {
        throw new Error('FeedMob API request failed: Bad Request');
      } else if (status === 404) {
        throw new Error('FeedMob API request failed: Not Found');
      } else {
        throw new Error(`FeedMob API request failed: ${status || 'Unknown error'}`);
      }
    }
    throw new Error('Failed to fetch data from FeedMob API');
  }
}
