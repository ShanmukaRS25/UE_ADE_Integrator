// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class UE_ADE_Demo : ModuleRules
{
	public UE_ADE_Demo(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"UE_ADE_Demo",
			"UE_ADE_Demo/Variant_Platforming",
			"UE_ADE_Demo/Variant_Platforming/Animation",
			"UE_ADE_Demo/Variant_Combat",
			"UE_ADE_Demo/Variant_Combat/AI",
			"UE_ADE_Demo/Variant_Combat/Animation",
			"UE_ADE_Demo/Variant_Combat/Gameplay",
			"UE_ADE_Demo/Variant_Combat/Interfaces",
			"UE_ADE_Demo/Variant_Combat/UI",
			"UE_ADE_Demo/Variant_SideScrolling",
			"UE_ADE_Demo/Variant_SideScrolling/AI",
			"UE_ADE_Demo/Variant_SideScrolling/Gameplay",
			"UE_ADE_Demo/Variant_SideScrolling/Interfaces",
			"UE_ADE_Demo/Variant_SideScrolling/UI"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
