#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { fetchInmobiCampaignMappingsData } from "./api.js";

// Create server instance
const server = new McpServer({
  name: "feedmob-spend",
  version: "0.0.1",
  capabilities: {
    tools: {},
    prompts: {},
  },
});

// Tool Definition
server.tool(
  "get_inmobi_campaign_mappings",
  "Get inmobi_campaign_mappings via FeedMob API.",
  {}, // No input parameters required for this endpoint
  async () => {
    try {
      const spendData = await fetchInmobiCampaignMappingsData();
      // Format the data nicely for the LLM/user
      const formattedData = JSON.stringify(spendData, null, 2);
      return {
        content: [{
          type: "text",
          text: `Spend data:\n\`\`\`json\n${formattedData}\n\`\`\``,
        }],
      };
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : "An unknown error occurred while fetching campaign mappings.";
      console.error("Error in get_spend_data tool:", errorMessage);
      return {
        content: [{ type: "text", text: `Error fetching spend data: ${errorMessage}` }],
        isError: true,
      };
    }
  }
);

// Prompt Definition
server.prompt(
  "check_spend_data",
  "Check spend data through the FeedMob API.",
  {},
  () => {
    return {
      messages: [{
        role: "user",
        content: {
          type: "text",
          text: "Please retrieve and summarize the spend data.",
        }
      }],
    };
  }
);

// Run the Server
async function main() {
  const transport = new StdioServerTransport();
  try {
    await server.connect(transport);
    console.error("FeedMob Spend MCP Server running on stdio...");
  } catch (error) {
    console.error("Failed to start FeedMob Spend MCP Server:", error);
    process.exit(1);
  }
}

main();
