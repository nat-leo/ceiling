import http from "k6/http";
import { check, sleep } from "k6";

const baseUrl = __ENV.BASE_URL || "http://localhost:8000";
const targetPath = __ENV.TARGET_PATH || "/";
const waitSeconds = Number(__ENV.WAIT_SECONDS || 0);

export const options = {
  thresholds: {
    http_req_failed: ["rate<0.05"],
    http_req_duration: ["p(95)<750"],
  },
  summaryTrendStats: ["avg", "min", "med", "p(90)", "p(95)", "max"],
};

export default function () {
  const response = http.get(`${baseUrl}${targetPath}`, {
    tags: { name: "constant-load" },
  });

  check(response, {
    "status is 200": (r) => r.status === 200,
  });

  sleep(waitSeconds);
}
