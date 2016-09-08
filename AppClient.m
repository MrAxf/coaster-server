#import "AppClient.h"

@interface ResultsViewController ()

@property (nonatomic, strong) NSString* urlbase;
@property (nonatomic, strong) NSString* userId;
- (NSDictionary) doRequest: (NSURL) url jsonString: (NSString) jsonRequest;

@end

@implementation AppClient

static AppClient *sharedClient = nil;

+ (AppClient *)sharedInstance{
  if (sharedClient == nil) {
    sharedClient = [[super allocWithZone:NULL] init];
  }
  return sharedAwardCenter;
}

- (instancetype) init{
  self = [super init];
  self.urlbase = @"http://localhost:5000";
  self.nameFilter = @"";
  self.typeFilter = @"";
  self.favFilter = @"";
  self.userId = @"";
}

- (NSDictionary)login:(NSString)email password:(NSString)password{

  NSString *jsonRequest = [NSString stringWithFormat:@"{\"email\": \"%@\", \"password\": \"%@\"}", email, password];
  NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@/%@", self.urlbase, @"login"]];
  NSDictionary *response = [self doRequest:url jsonString:jsonRequest];
  self.userId = response[@"id"];
  return response;

}

- (NSDictionary)reg:(NSString)email password:(NSString)password{

  NSString *jsonRequest = [NSString stringWithFormat:@"{\"email\": \"%@\", \"password\": \"%@\"}", email, password];
  NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@/%@", self.urlbase, @"register"]];
  return [self doRequest:url jsonString:jsonRequest];

}

- (NSDictionary)getCoasters{

  NSString *jsonRequest = [NSString stringWithFormat:@"{\"userId\": \"%@\", \"nameFilter\": \"%@\", \"typeFilter\": \"%@\", \"favFilter\": \"%@\"}", self.userId, self.nameFilter, self.typeFilter, self.favFilter];
  NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@/%@", self.urlbase, @"coasters"]];
  return [self doRequest:url jsonString:jsonRequest];

}

- (NSDictionary)getCoaster:(NSString)id{

  NSString *jsonRequest = [NSString stringWithFormat:@"{\"userId\": \"%@\"}", self.userId];
  NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@/%@/%@", self.urlbase, @"coasters", id]];
  return [self doRequest:url jsonString:jsonRequest];

}

- (NSDictionary)addCoaster:(NSString)nombre tipo:(NSString)tipo altura:(NSNumber)altura velocidad:(NSNumber)velocidad glateral:(NSNumber)glateral maxgvertical:(NSNumber)maxgvertical mingvertical:(NSNumber)mingvertical loops:(NSNumber)loops dropsloops:(NSNumber)drops{

  NSString *jsonRequest = [NSString stringWithFormat:@"{\"userId\": \"%@\", \"nombre\": \"%@\", \"tipo\": \"%@\", \"velocidad\": \"%@\", \"glateral\": \"%@\", \"maxgvertical\": \"%@\", \"mingvertical\": \"%@\", \"loops\": \"%@\", \"drops\": \"%@\"}", self.userId, nombre, tipo, [altura stringValue], [velocidad stringValue], [glateral stringValue], [maxgvertical stringValue], [mingvertical stringValue], [loops stringValue], [drops stringValue]];
  NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@/%@/post", self.urlbase, @"coasters"]];
  return [self doRequest:url jsonString:jsonRequest];

}

- (NSDictionary)addCoaster:(NSString)id nombre:(NSString)nombre tipo:(NSString)tipo altura:(NSNumber)altura velocidad:(NSNumber)velocidad glateral:(NSNumber)glateral maxgvertical:(NSNumber)maxgvertical mingvertical:(NSNumber)mingvertical loops:(NSNumber)loops dropsloops:(NSNumber)drops{

  NSString *jsonRequest = [NSString stringWithFormat:@"{\"userId\": \"%@\", \"nombre\": \"%@\", \"tipo\": \"%@\", \"velocidad\": \"%@\", \"glateral\": \"%@\", \"maxgvertical\": \"%@\", \"mingvertical\": \"%@\", \"loops\": \"%@\", \"drops\": \"%@\"}", self.userId, nombre, tipo, [altura stringValue], [velocidad stringValue], [glateral stringValue], [maxgvertical stringValue], [mingvertical stringValue], [loops stringValue], [drops stringValue]];
  NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@/%@/%@/updtae", self.urlbase, @"coasters", id]];
  return [self doRequest:url jsonString:jsonRequest];

}

- (NSDictionary)delCoaster:(NSString)id{

  NSString *jsonRequest = [NSString stringWithFormat:@"{\"userId\": \"%@\"}", self.userId];
  NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@/%@/%@/delete", self.urlbase, @"coasters", id]];
  return [self doRequest:url jsonString:jsonRequest];

}

- (NSDictionary)commentCoaster:(NSString)id comment:(NSString)comment{

  NSString *jsonRequest = [NSString stringWithFormat:@"{\"userId\": \"%@\", \"comment\": \"%@\"}", self.userId, comment];
  NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@/%@/%@/comment", self.urlbase, @"coasters", id]];
  return [self doRequest:url jsonString:jsonRequest];

}

- (NSDictionary)likeCoaster:(NSString)id{

  NSString *jsonRequest = [NSString stringWithFormat:@"{\"userId\": \"%@\"}", self.userId];
  NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@/%@/%@/like", self.urlbase, @"coasters", id]];
  return [self doRequest:url jsonString:jsonRequest];

}
- (NSDictionary)favCoaster:(NSString)id{

  NSString *jsonRequest = [NSString stringWithFormat:@"{\"userId\": \"%@\"}", self.userId];
  NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@/%@/%@/fav", self.urlbase, @"coasters", id]];
  return [self doRequest:url jsonString:jsonRequest];

}

- (NSDictionary) doRequest: (NSURL) url jsonString: (NSString) jsonRequest{

  NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url
  cachePolicy:NSURLRequestUseProtocolCachePolicy timeoutInterval:60.0];

  NSData *requestData = [jsonRequest dataUsingEncoding:NSUTF8StringEncoding];

  [request setHTTPMethod:@"POST"];
  [request setValue:@"application/json" forHTTPHeaderField:@"Accept"];
  [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
  [request setValue:[NSString stringWithFormat:@"%d", [requestData length]] forHTTPHeaderField:@"Content-Length"];
  [request setHTTPBody: requestData];

  NSError *error = [[NSError alloc] init];
  NSHTTPURLResponse *responseCode = nil;

  NSData *responseData = [NSURLConnection sendSynchronousRequest:request returningResponse:&responseCode error:&error];

  if([responseCode statusCode] != 200){
      NSLog(@"Error getting %@, HTTP status code %i", url, [responseCode statusCode]);
      return nil;
  }

  NSString *jsonString = [[NSString alloc] initWithData:oResponseData encoding:NSUTF8StringEncoding];
  return [jsonString JSONValue];
}

// singleton methods
+ (id)allocWithZone:(NSZone *)zone {
  return [[self sharedClient] retain];
}

- (id)copyWithZone:(NSZone *)zone {
  return self;
}

- (id)retain {
  return self;
}

- (NSUInteger)retainCount {
  return NSUIntegerMax;
}

- (void)release {

}

- (id)autorelease {
  return self;
}

-(void)dealloc {
  [super dealloc];
}

@end
