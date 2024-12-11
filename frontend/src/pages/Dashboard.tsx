// frontend/src/pages/Dashboard.tsx
import React, { useState, useEffect } from 'react';
import { newsService } from '../services/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Skeleton } from '@/components/ui/skeleton';
import { AlertCircle } from 'lucide-react';

interface GlobalPerspective {
  title: string;
  summary: string;
  sources: string[];
  keywords: string[];
}

interface NewsAggregationData {
  total_articles: number;
  topic_clusters: number;
  global_perspectives: GlobalPerspective[];
}

const Dashboard: React.FC = () => {
  const [newsData, setNewsData] = useState<NewsAggregationData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true);
        const data = await newsService.aggregateNews();
        setNewsData(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch news. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
    // Optional: Set up periodic refresh
    const intervalId = setInterval(fetchNews, 15 * 60 * 1000); // Refresh every 15 minutes
    return () => clearInterval(intervalId);
  }, []);

  if (loading) {
    return (
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Global News Dashboard</h1>
        {[1, 2, 3].map((_, index) => (
          <Skeleton key={index} className="h-40 w-full mb-4" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-4 text-center text-red-500">
        <AlertCircle className="mx-auto mb-4" size={48} />
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Global News Perspectives</h1>
        <div className="flex space-x-4 mt-2">
          <Badge variant="outline">
            Total Articles: {newsData?.total_articles}
          </Badge>
          <Badge variant="outline">
            Topic Clusters: {newsData?.topic_clusters}
          </Badge>
        </div>
      </div>

      <Tabs defaultValue="perspectives" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="perspectives">Global Perspectives</TabsTrigger>
          <TabsTrigger value="sources">News Sources</TabsTrigger>
          <TabsTrigger value="keywords">Key Topics</TabsTrigger>
        </TabsList>

        <TabsContent value="perspectives">
          {newsData?.global_perspectives.map((perspective, index) => (
            <Card key={index} className="mb-4">
              <CardHeader>
                <CardTitle>{perspective.title}</CardTitle>
                <div className="flex flex-wrap gap-2 mt-2">
                  {perspective.sources.map((source) => (
                    <Badge key={source} variant="secondary">
                      {source}
                    </Badge>
                  ))}
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">{perspective.summary}</p>
                <div className="mt-4 flex flex-wrap gap-2">
                  {perspective.keywords.map((keyword) => (
                    <Badge key={keyword} variant="outline">
                      {keyword}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        <TabsContent value="sources">
          <Card>
            <CardHeader>
              <CardTitle>News Sources</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {newsData?.global_perspectives
                  .flatMap((p) => p.sources)
                  .filter((source, index, self) => self.indexOf(source) === index)
                  .map((source) => (
                    <Badge key={source} variant="outline">
                      {source}
                    </Badge>
                  ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="keywords">
          <Card>
            <CardHeader>
              <CardTitle>Key Topics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {newsData?.global_perspectives
                  .flatMap((p) => p.keywords)
                  .filter((keyword, index, self) => self.indexOf(keyword) === index)
                  .map((keyword) => (
                    <Badge key={keyword} variant="outline">
                      {keyword}
                    </Badge>
                  ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Dashboard;
