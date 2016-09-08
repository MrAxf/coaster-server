#import <UIKit/UIKit.h>

@interface ApiClient : NSObject

@property NSString* nameFilter;
@property NSString* typeFilter;
@property NSString* likeFilter;
@property NSString* favFilter;

+ (AppClient *)sharedInstance
- (NSDictionary)login:(NSString)email password:(NSString)password;
- (NSDictionary)reg:(NSString)email password:(NSString)password;
- (NSDictionary)getCoasters;
- (NSDictionary)getCoaster:(NSString)id;
- (NSDictionary)addCoaster:(NSString)nombre tipo:(NSString)tipo altura:(NSNumber)altura velocidad:(NSNumber)velocidad glateral:(NSNumber)glateral maxgvertical:(NSNumber)maxgvertical mingvertical:(NSNumber)mingvertical loops:(NSNumber)loops dropsloops:(NSNumber)drops;
- (NSDictionary)updateCoaster:(NSString)id nombre:(NSString)nombre tipo:(NSString)tipo altura:(NSNumber)altura velocidad:(NSNumber)velocidad glateral:(NSNumber)glateral maxgvertical:(NSNumber)maxgvertical mingvertical:(NSNumber)mingvertical loops:(NSNumber)loops dropsloops:(NSNumber)drops;
- (NSDictionary)delCoaster:(NSString)id;
- (NSDictionary)delCoaster:(NSString)id;
- (NSDictionary)likeCoaster:(NSString)id;
- (NSDictionary)favCoaster:(NSString)id;

@end
